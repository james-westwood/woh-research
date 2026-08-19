import collections
import html
import json
import os
import re
import unicodedata
from urllib.parse import quote
from data import ELECTRONIC, SOUL_JAZZ, VERIFIED, NOTE, BLURBS

TOTAL = len(ELECTRONIC) + len(SOUL_JAZZ)

# Snapshots of the official timetable and the festival's own artist blurbs.
# Regenerate with fetch_official.py; build.py itself never touches the network.
def _load(path, default):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        print(f'  note: {path} missing, artist pages will be thinner')
        return default

OFFICIAL = _load('official_schedule.json', [])
BIOS = _load('artist_bios.json', {})

STOPWORDS = {'live', 'dj', 'set', 'b2b', 'ft', 'feat', 'featuring', 'presents', 'with',
             'the', 'and', 'a', 'vs', 'x'}

def name_tokens(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r'\(.*?\)', ' ', s)
    return {t for t in re.split(r'[^a-z0-9]+', s) if len(t) > 1 and t not in STOPWORDS}

def slug(name):
    s = unicodedata.normalize('NFKD', name)
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s or 'artist'

def bio_for(name):
    """Our own blurb if we wrote one, otherwise the festival's.

    Returns (text, sources) where sources is None for the festival's own copy,
    so the page can say plainly whose words these are.
    """
    ours = BLURBS.get(name)
    if ours:
        return ours['text'], ours.get('sources') or []

    want = name_tokens(name)
    if not want:
        return None, None
    for official_name, text in BIOS.items():
        if name_tokens(official_name) == want:
            return text, None
    for official_name, text in BIOS.items():
        if want <= name_tokens(official_name):
            return text, None
    return None, None

def official_sets_for(name, day=None, time=None, stage=None):
    """Every official set this artist appears in, b2b billings included.

    Name tokens find the extra sets, but they miss billings that share no word
    with ours ("V.I.V.E.K" is all single letters; Jazzanova's "In Between" show
    is billed plain). Our own slot is known-good because verify.py checks it on
    day plus stage plus start, so add that back in regardless.
    """
    want = name_tokens(name)
    hits = []
    if want and len(''.join(sorted(want))) >= 3:
        hits = [r for r in OFFICIAL if want <= name_tokens(r['artist'])]
    if day and time and stage:
        start = time.partition('-')[0]
        ours = next((r for r in OFFICIAL if r['day'] == day and r['stage'] == stage
                     and r['start'] == start), None)
        if ours is not None and ours not in hits:
            hits.append(ours)
    return sorted(hits, key=lambda r: (DAY_ORDER.get(r['day'], 9), start_minutes(r['start'])))

ELEC_CATS = [
    ('Techno', ['techno', 'acid']),
    ('House', ['house']),
    ('Garage / Bass', ['garage', 'bass', 'grime', 'gqom', 'ukg', 'dubstep']),
    ('D&B / Jungle', ['drum & bass', 'jungle', 'halftime']),
    ('Dub / Reggae', ['dub', 'steppers', 'reggae', 'dancehall']),
    ('Electro / Broken Beat', ['broken beat', 'electro', 'experimental', 'electronic', 'ambient']),
    ('Disco / Boogie', ['disco', 'boogie', 'edits']),
    ('Eclectic / Global', ['eclectic', 'global', 'afro', 'balearic', 'brazilian', 'nu-jazz',
                           'north african', 'latin', 'soul', 'funk', 'hip-hop']),
    # Additive, and deliberately overlapping the buckets above: the African and
    # diaspora club sounds are spread across Garage / Bass (gqom), House
    # (afro-house) and Eclectic / Global (north african), so there was no single
    # filter that collected them. Categories are multi-label, so nothing moves.
    ('Afro / Diaspora club', ['afro', 'gqom', 'north african', 'kwaito', 'amapiano',
                              'afrobeats', 'highlife', 'bruk']),
]

SJ_CATS = [
    ('Jazz', ['jazz', 'warriors showcase', 'classical', 'improv']),
    ('Soul / R&B', ['soul', 'r&b', 'neo-soul']),
    ('Hip-hop / Rap', ['hip-hop', 'rap', 'spoken word', 'poetry']),
    ('Afrobeat / Global', ['afro', 'global', 'brazilian', 'tanzanian', 'orchestral', 'latin',
                           'ethio', 'reggae', 'dub']),
    ('Live band / Fusion', ['funk', 'fusion', 'live', 'alt', 'pop', 'experimental', 'tribute',
                            'band', 'rock', 'electronic']),
]

def categorize(tag, catmap):
    t = tag.lower()
    cats = [label for label, kws in catmap if any(kw in t for kw in kws)]
    return cats or ['Other']

def esc(s):
    """Escape for both text nodes and double-quoted attributes."""
    return html.escape(str(s), quote=True)

def base_name(name):
    clean = re.sub(r'\(.*?\)', '', name)
    clean = re.sub(r'\b(ft|feat|b2b|presents|with)\b.*', '', clean, flags=re.I)
    return clean.strip()

def sc_search(name):
    return f"https://soundcloud.com/search?q={quote(base_name(name))}"

def mc_search(name):
    # /search/?q= and /search?q= both 301 to the Mixcloud homepage and throw the
    # query away, which is why the phone app ended up searching for "search".
    # /search/cloudcasts/?q= is the one that survives, and cloudcasts means mixes.
    return f"https://www.mixcloud.com/search/cloudcasts/?q={quote(base_name(name))}"

def yt_search(name):
    """A link the phone apps do honour, for when SoundCloud's swallows the query."""
    return ("https://www.youtube.com/results?search_query="
            + quote(base_name(name) + ' dj mix'))

DAYS = ['Thu', 'Fri', 'Sat', 'Sun']
DAY_NAMES = {'Thu': 'Thu 20', 'Fri': 'Fri 21', 'Sat': 'Sat 22', 'Sun': 'Sun 23'}
DAY_ORDER = {d: i for i, d in enumerate(DAYS)}

# A festival day does not end at midnight. Saturday at The Grove runs I-Sha
# 20:00, Shackleton 22:00, re:ni 23:00-01:00, Blawan 01:00, Nono Gigsta
# 02:00-04:00: one continuous night. So a set starting before this hour belongs
# at the END of its day's running order, not the start. Nothing in the data
# starts between 04:00 and 11:00, so the boundary is unambiguous.
ROLLOVER_HOUR = 6

def start_minutes(time):
    """Minutes from the start of the festival day, rolling small hours past midnight."""
    h, m = int(time[:2]), int(time[3:5])
    return h * 60 + m + (24 * 60 if h < ROLLOVER_HOUR else 0)

def running_order(items):
    """Chronological: day, then time within that day's programme."""
    return sorted(items, key=lambda it: (DAY_ORDER[it[2]], start_minutes(it[3]), it[0].lower()))

def set_html(name, tag, day, time, stage, catmap):
    cats = categorize(tag, catmap)
    verified = VERIFIED.get(re.sub(r'\s*\(.*?\)', '', name).strip())
    start, _, end = time.partition('-')

    links = ''
    if verified:
        links += (f'<a class="btn btn--play" href="{esc(verified)}" target="_blank" rel="noopener">'
                  f'<span aria-hidden="true">&#9654;</span> Play mix</a>')
    links += (f'<a class="btn" href="{esc(sc_search(name))}" target="_blank" rel="noopener">'
              f'Search SoundCloud</a>')
    links += (f'<a class="btn" href="{esc(mc_search(name))}" target="_blank" rel="noopener">'
              f'Search Mixcloud</a>')
    links += (f'<a class="btn" href="{esc(yt_search(name))}" target="_blank" rel="noopener">'
              f'Search YouTube</a>')

    return f'''<article class="set" data-day="{esc(day)}" data-cat="{esc('|'.join(cats))}" data-stage="{esc(stage)}" data-name="{esc(name.lower())}">
      <div class="clock">
        <span class="clock-start">{esc(start)}</span>
        <span class="clock-end">{esc(end)}</span>
      </div>
      <div class="set-main">
        <h3 class="set-name"><a href="artists/{slug(name)}.html">{esc(name)}</a></h3>
        <p class="set-where">
          <span class="where-day">{esc(DAY_NAMES[day])}</span>
          <span class="where-tag">{esc(tag)}</span>
          <span class="where-stage">{esc(stage)}</span>
        </p>
        <div class="set-links">{links}</div>
      </div>
    </article>'''

def chips_html(catmap):
    return ''.join(
        f'<button type="button" class="chip" data-filter="{esc(label)}" aria-pressed="false">{esc(label)}</button>'
        for label, _ in catmap
    )

def stage_chips_html(items):
    """Only the stages this list actually uses, busiest first."""
    counts = collections.Counter(it[4] for it in items)
    stages = sorted(counts, key=lambda s: (-counts[s], s.lower()))
    return ''.join(
        f'<button type="button" class="chip" data-stage-filter="{esc(s)}" aria-pressed="false">{esc(s)}</button>'
        for s in stages
    )

def day_chips_html():
    return ''.join(
        f'<button type="button" class="chip" data-day-filter="{esc(d)}" aria-pressed="false">{esc(DAY_NAMES[d])}</button>'
        for d in DAYS
    )

def wall_html():
    """Every name on the bill, alphabetical, each linking to its own artist page."""
    seen = {}
    for items, page in ((ELECTRONIC, 'electronic.html'), (SOUL_JAZZ, 'soul-jazz-afro.html')):
        for name, *_ in items:
            seen.setdefault(name, page)
    names = sorted(seen, key=lambda n: n.lower())
    # Joined on newlines so the browser has somewhere to break the line.
    return '\n'.join(
        f'<a class="wall-name" href="artists/{slug(n)}.html">{esc(n)}</a>'
        for n in names
    )

CSS = '''
/* ==========================================================================
   We Out Here: Do Your Own Research
   "Set Times" — a screen-printed festival bill crossed with a radio schedule.
   Two exposures of one identity: chalk downland by day, ink by night.
   Ultramarine = you can press it. Marigold = worth your attention.
   ========================================================================== */

body {
  --paper:      #e7e9e2;
  --surface:    #f5f5f1;
  --surface-2:  #eceee6;
  --ink:        #121926;
  --ink-2:      #4c5666;
  --muted:      #646d7b;
  --rule:       #d2d5cc;
  --blue:       #2438ce;
  --blue-ink:   #ffffff;
  /* Marigold reads as a fill, not as text: on chalk it needs a darker cut to
     stay legible, so --sun paints backgrounds and --sun-text sets type. */
  --sun:        #f0a81e;
  --sun-ink:    #1a1200;
  --sun-text:   #96590a;

  --display: "Big Shoulders Display", "Archivo Narrow", "Haettenschweiler",
             "Arial Narrow", system-ui, sans-serif;
  --body: "Archivo", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, "SF Mono", "Cascadia Mono", monospace;

  color-scheme: light;
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--body);
  font-size: 16px;
  line-height: 1.45;
  -webkit-text-size-adjust: 100%;
  overflow-x: clip; /* the hero photo bleeds to 100vw */
}

@media (prefers-color-scheme: dark) {
  body:where(:not([data-theme="light"])) {
    --paper:     #0d1320;
    --surface:   #151d2b;
    --surface-2: #111826;
    --ink:       #f3f2eb;
    --ink-2:     #a8b1bf;
    --muted:     #7d8899;
    --rule:      #212b3b;
    --blue:      #6d7dff;
    --blue-ink:  #0b1020;
    --sun:       #f7bc42;
    --sun-ink:   #14100a;
    --sun-text:  #f7bc42;
    color-scheme: dark;
  }
}

body[data-theme="dark"] {
  --paper:     #0d1320;
  --surface:   #151d2b;
  --surface-2: #111826;
  --ink:       #f3f2eb;
  --ink-2:     #a8b1bf;
  --muted:     #7d8899;
  --rule:      #212b3b;
  --blue:      #6d7dff;
  --blue-ink:  #0b1020;
  --sun:       #f7bc42;
  --sun-ink:   #14100a;
  --sun-text:  #f7bc42;
  color-scheme: dark;
}

* { box-sizing: border-box; }

:focus-visible {
  outline: 2px solid var(--blue);
  outline-offset: 2px;
  border-radius: 2px;
}

.wrap { max-width: 1040px; margin: 0 auto; padding: 28px 18px 72px; }

/* --- landing hero: the main stage at dusk ------------------------------- */

/* The photo is small, so it is treated as atmosphere rather than a picture:
   bled full width, faded right down, softened, and masked out to bare paper
   before the bill starts. Keeps the type doing the work. */
.hero { position: relative; }
.hero > * { position: relative; z-index: 1; }
.hero::before {
  content: "";
  position: absolute;
  z-index: 0;
  top: -28px;
  left: 50%;
  width: 100vw;
  height: calc(100% + 28px);
  transform: translateX(-50%);
  background: url("main_stage.jpg") 50% 64% / cover no-repeat;
  opacity: 0.22;
  filter: blur(1px) saturate(0.9);
  -webkit-mask-image: linear-gradient(to bottom, #000 0%, #000 52%, transparent 96%);
          mask-image: linear-gradient(to bottom, #000 0%, #000 52%, transparent 96%);
  pointer-events: none;
}
@media (prefers-color-scheme: dark) {
  body:where(:not([data-theme="light"])) .hero::before { opacity: 0.34; }
}
body[data-theme="dark"] .hero::before { opacity: 0.34; }

/* --- masthead ----------------------------------------------------------- */

.masthead {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
  padding-bottom: 18px;
  border-bottom: 2px solid var(--ink);
}
.eyebrow {
  font-family: var(--mono);
  font-size: 10.5px;
  font-weight: 500;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--ink-2);
  margin: 0 0 10px;
}
.wordmark {
  font-family: var(--display);
  font-weight: 800;
  font-size: clamp(38px, 11vw, 82px);
  line-height: 0.86;
  letter-spacing: -0.005em;
  text-transform: uppercase;
  margin: 0;
  color: var(--ink);
}
.wordmark .research { display: block; color: var(--sun-text); }

/* Interior pages carry a smaller mark so the listing gets the room. */
.masthead--inner { border-bottom-width: 1px; padding-bottom: 14px; }
.masthead--inner .wordmark { font-size: clamp(30px, 6vw, 46px); }

.toggle-btn {
  flex: none;
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 8px 11px;
  border-radius: 999px;
  border: 1px solid var(--rule);
  background: var(--surface);
  color: var(--ink-2);
  cursor: pointer;
}
.toggle-btn:hover { border-color: var(--blue); color: var(--blue); }

/* --- landing: the standfirst and the name wall -------------------------- */

.standfirst {
  font-size: clamp(16px, 2.4vw, 20px);
  line-height: 1.4;
  max-width: 30em;
  margin: 26px 0 0;
  color: var(--ink);
}
.standfirst b { color: var(--sun-text); font-weight: 700; }
.standfirst-sub {
  font-size: 14.5px;
  line-height: 1.55;
  max-width: 34em;
  color: var(--ink-2);
  margin: 10px 0 0;
}

.wall-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  font-family: var(--mono);
  font-size: 10.5px;
  font-weight: 500;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 40px 0 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--rule);
}

.wall {
  font-family: var(--display);
  font-weight: 700;
  font-size: clamp(16px, 2.3vw, 22px);
  line-height: 1.22;
  text-transform: uppercase;
  letter-spacing: 0.005em;
}
.wall-name {
  color: var(--ink-2);
  text-decoration: none;
  transition: color 0.12s ease;
}
.wall-name:hover,
.wall-name:focus-visible { color: var(--sun-text); }
/* Names run on like a printed bill, so each needs its own stop. The separator
   rides on the name before it, so a line never starts with a stray dot. */
.wall-name:not(:last-child)::after {
  content: "\\00b7";
  margin-left: 0.42em;
  color: var(--rule);
}

/* --- landing: the two lists --------------------------------------------- */

.lists { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 44px; }
.list-tile {
  display: block;
  padding: 22px 22px 24px;
  border: 1px solid var(--rule);
  border-radius: 4px;
  background: var(--surface);
  text-decoration: none;
  transition: border-color 0.12s ease, transform 0.12s ease;
}
.list-tile:hover,
.list-tile:focus-visible { border-color: var(--blue); transform: translateY(-2px); }
.list-count {
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--blue);
}
.list-tile h2 {
  font-family: var(--display);
  font-weight: 700;
  font-size: clamp(24px, 3.6vw, 34px);
  line-height: 1;
  text-transform: uppercase;
  margin: 8px 0 8px;
  color: var(--ink);
}
.list-tile p { margin: 0; font-size: 13.5px; line-height: 1.5; color: var(--ink-2); }

/* --- interior: nav, search, filters ------------------------------------- */

nav.pagenav { display: flex; flex-wrap: wrap; gap: 6px; margin: 18px 0 22px; }
nav.pagenav a {
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: 8px 13px;
  border-radius: 999px;
  text-decoration: none;
  border: 1px solid var(--rule);
  color: var(--ink-2);
}
nav.pagenav a:hover { border-color: var(--blue); color: var(--blue); }
nav.pagenav a.active {
  background: var(--ink);
  color: var(--paper);
  border-color: var(--ink);
}

.searchbox {
  width: 100%;
  max-width: 26em;
  padding: 12px 15px;
  font-family: var(--body);
  font-size: 15px;
  border-radius: 4px;
  border: 1px solid var(--rule);
  background: var(--surface);
  color: var(--ink);
  margin-bottom: 18px;
}
.searchbox::placeholder { color: var(--muted); }
.searchbox:focus { border-color: var(--blue); outline-offset: 1px; }

.chipgroup { display: flex; align-items: baseline; gap: 12px; margin-bottom: 10px; }
.chiplabel {
  flex: none;
  width: 4.2em;
  font-family: var(--mono);
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.11em;
  text-transform: uppercase;
  color: var(--muted);
  padding-top: 7px;
}
.chips { display: flex; gap: 6px; flex-wrap: wrap; }
.chip {
  font-family: var(--body);
  font-size: 12px;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid var(--rule);
  background: transparent;
  color: var(--ink-2);
  cursor: pointer;
}
.chip:hover { border-color: var(--blue); color: var(--blue); }
.chip[aria-pressed="true"] {
  background: var(--blue);
  color: var(--blue-ink);
  border-color: var(--blue);
  font-weight: 600;
}

.tally {
  display: flex;
  align-items: baseline;
  gap: 10px;
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 22px 0 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--rule);
}
.btn-clear {
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: none;
  border: 0;
  padding: 0;
  color: var(--blue);
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 3px;
}

/* --- interior: the set list, on a time spine ---------------------------- */

.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 44px; }

.set {
  display: flex;
  gap: 14px;
  padding: 15px 0;
  border-bottom: 1px solid var(--rule);
}
/* Required: a class-based display beats the browser's own [hidden] rule, so
   without this the filters compute correctly but nothing ever disappears. */
.set[hidden] { display: none; }

/* The clock rail is the structure: start over end, monospaced so the
   columns line up down the page like a printed schedule. */
.clock {
  flex: none;
  width: 3.4em;
  font-family: var(--mono);
  font-variant-numeric: tabular-nums;
  padding-top: 2px;
}
.clock-start { display: block; font-size: 14px; font-weight: 500; color: var(--ink); }
.clock-end { display: block; font-size: 11.5px; color: var(--muted); }
.clock-end::before { content: "\\2013\\00a0"; }

.set-main { min-width: 0; }
.set-name {
  font-family: var(--display);
  font-weight: 700;
  font-size: clamp(20px, 2.5vw, 26px);
  line-height: 1;
  text-transform: uppercase;
  margin: 0 0 5px;
  overflow-wrap: break-word;
}
.set-name a {
  color: var(--ink);
  text-decoration: none;
  text-decoration-color: var(--rule);
}
.set-name a:hover,
.set-name a:focus-visible { color: var(--sun-text); text-decoration: underline; }

/* --- one artist: the festival's blurb, and every set they play ----------- */

.artist {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 21em;
  gap: 44px;
  margin-top: 4px;
}
.bio p { font-size: 15.5px; line-height: 1.62; color: var(--ink-2); margin: 0 0 14px; max-width: 62ch; }
.bio p:first-child { font-size: 17px; color: var(--ink); }
.bio-source, .bio-none { font-size: 12px; color: var(--muted); }
.bio-source a { color: var(--muted); }
.bio-none { font-size: 14px; }

.side { border-top: 2px solid var(--ink); padding-top: 14px; }
.side-head {
  font-family: var(--mono);
  font-size: 10.5px;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 12px;
}
.side-note { font-size: 11.5px; line-height: 1.5; color: var(--muted); margin: 12px 0 0; }

.gigs { list-style: none; margin: 0; padding: 0; }
.gig {
  display: grid;
  gap: 1px 8px;
  padding: 10px 0 10px 11px;
  border-bottom: 1px solid var(--rule);
  border-left: 2px solid transparent;
}
/* the slot carried on the list pages, so both views agree */
.gig--ours { border-left-color: var(--sun); }
.gig-when { font-size: 13px; font-weight: 600; color: var(--ink); }
.gig-time {
  font-family: var(--mono);
  font-variant-numeric: tabular-nums;
  font-size: 12.5px;
  color: var(--ink-2);
}
.gig-stage { font-size: 12px; color: var(--muted); }
.billed { font-size: 11.5px; color: var(--sun-text); }

.artist .set-links { margin-top: 16px; }
.set-where {
  display: flex;
  flex-wrap: wrap;
  gap: 0 7px;
  font-size: 12px;
  color: var(--ink-2);
  margin: 0 0 9px;
}
.where-day { font-family: var(--mono); font-size: 11px; color: var(--muted); }
.where-tag { color: var(--ink-2); }
.where-tag::before,
.where-stage::before { content: "\\00b7\\00a0"; color: var(--muted); }
.where-stage { color: var(--muted); }

.set-links { display: flex; gap: 6px; flex-wrap: wrap; }
.btn {
  font-family: var(--body);
  font-size: 11.5px;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 3px;
  border: 1px solid var(--rule);
  background: var(--surface-2);
  color: var(--ink-2);
  text-decoration: none;
  white-space: nowrap;
}
.btn:hover { border-color: var(--blue); color: var(--blue); }
.btn--play {
  background: var(--sun);
  border-color: var(--sun);
  color: var(--sun-ink);
  font-weight: 700;
}
.btn--play:hover { color: var(--sun-ink); border-color: var(--ink); }

.empty { font-size: 14px; color: var(--ink-2); padding: 44px 0; }

/* --- footer matter ------------------------------------------------------ */

/* Set in two columns so the small print fills the measure without running to
   an unreadable line length. */
.note {
  font-size: 12px;
  color: var(--muted);
  line-height: 1.65;
  margin: 44px 0 0;
  padding-top: 18px;
  border-top: 1px solid var(--rule);
  column-count: 2;
  column-gap: 44px;
}
footer.credit {
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--muted);
  margin-top: 30px;
}

/* --- narrow ------------------------------------------------------------- */

@media (max-width: 760px) {
  .grid { grid-template-columns: 1fr; gap: 0; }
  .lists { grid-template-columns: 1fr; }
  .wrap { padding: 22px 15px 60px; }
  .chipgroup { flex-direction: column; gap: 5px; }
  .chiplabel { width: auto; padding-top: 0; }
  .wall { font-size: 15px; }
  .note { column-count: 1; }
  /* in a field the set times matter more than the reading, so lead with them */
  .artist { grid-template-columns: 1fr; gap: 26px; }
  .artist .side { order: -1; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  .list-tile:hover { transform: none; }
}
'''

JS = '''
(function () {
  'use strict';

  var body = document.body;
  var toggle = document.getElementById('toggleTheme');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      body.setAttribute('data-theme', next);
      try { localStorage.setItem('woh-theme', next); } catch (e) {}
    });
  }

  var sets = Array.prototype.slice.call(document.querySelectorAll('.set'));
  if (!sets.length) return;

  var total = sets.length;
  var search = document.getElementById('search');
  var tally = document.getElementById('tally');
  var clearBtn = document.getElementById('clearFilters');
  var emptyMsg = document.getElementById('emptyMsg');
  var dayBtns = Array.prototype.slice.call(document.querySelectorAll('[data-day-filter]'));
  var catBtns = Array.prototype.slice.call(document.querySelectorAll('[data-filter]'));
  var stageBtns = Array.prototype.slice.call(document.querySelectorAll('[data-stage-filter]'));

  var activeDay = null;
  var activeCats = [];
  var activeStages = [];
  var term = '';

  function apply() {
    var visible = 0;
    sets.forEach(function (el) {
      var cats = el.getAttribute('data-cat').split('|');
      var dayOk = !activeDay || el.getAttribute('data-day') === activeDay;
      // Several sounds per set, so any selected sound matching is enough.
      var catOk = !activeCats.length || cats.some(function (c) { return activeCats.indexOf(c) !== -1; });
      var stageOk = !activeStages.length || activeStages.indexOf(el.getAttribute('data-stage')) !== -1;
      var nameOk = !term || el.getAttribute('data-name').indexOf(term) !== -1;
      var show = dayOk && catOk && stageOk && nameOk;
      el.hidden = !show;
      if (show) visible++;
    });

    var filtered = visible !== total;
    tally.textContent = filtered
      ? visible + ' of ' + total + ' sets'
      : total + ' sets';
    clearBtn.hidden = !filtered;
    emptyMsg.hidden = visible !== 0;
  }

  dayBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var d = btn.getAttribute('data-day-filter');
      var turningOff = activeDay === d;
      dayBtns.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
      activeDay = turningOff ? null : d;
      if (!turningOff) btn.setAttribute('aria-pressed', 'true');
      apply();
    });
  });

  catBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      var i = activeCats.indexOf(f);
      if (i !== -1) { activeCats.splice(i, 1); btn.setAttribute('aria-pressed', 'false'); }
      else { activeCats.push(f); btn.setAttribute('aria-pressed', 'true'); }
      apply();
    });
  });

  stageBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var s = btn.getAttribute('data-stage-filter');
      var i = activeStages.indexOf(s);
      if (i !== -1) { activeStages.splice(i, 1); btn.setAttribute('aria-pressed', 'false'); }
      else { activeStages.push(s); btn.setAttribute('aria-pressed', 'true'); }
      apply();
    });
  });

  search.addEventListener('input', function () {
    term = search.value.trim().toLowerCase();
    apply();
  });

  clearBtn.addEventListener('click', function () {
    activeDay = null;
    activeCats = [];
    activeStages = [];
    term = '';
    search.value = '';
    dayBtns.concat(catBtns, stageBtns).forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
    apply();
    search.focus();
  });

  // Names on the landing wall deep-link here as ?q=<artist>.
  var q = new URLSearchParams(window.location.search).get('q');
  if (q) {
    search.value = q;
    term = q.trim().toLowerCase();
  }

  apply();
})();
'''

# Set the stored theme before first paint so the page never flashes the wrong one.
THEME_BOOT = '''<script>
try { var t = localStorage.getItem('woh-theme'); if (t) document.body.setAttribute('data-theme', t); } catch (e) {}
</script>'''

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Big+Shoulders+Display:wght@500;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap">'''

FOOTER = ('We Out Here, 20&#8211;23 Aug 2026, Wimborne St Giles &middot; '
          'built for the group chats, not official festival material')

def head(title, description):
    return f'''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#e7e9e2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0d1320" media="(prefers-color-scheme: dark)">
{FONTS}
<link rel="stylesheet" href="style.css">'''

def build_page(title, standfirst, items, catmap, active_nav):
    items = running_order(items)
    rows = '\n'.join(set_html(*it, catmap) for it in items)
    desc = f'{standfirst} Every set at We Out Here 2026, with a mix to listen to first.'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
{head(f'{title} &mdash; We Out Here: Do Your Own Research', desc)}
</head>
<body>
{THEME_BOOT}
<div class="wrap">
  <header class="masthead masthead--inner">
    <div>
      <p class="eyebrow">We Out Here 2026 &middot; do your own research</p>
      <h1 class="wordmark">{title}</h1>
    </div>
    <button type="button" class="toggle-btn" id="toggleTheme">Day / night</button>
  </header>

  <nav class="pagenav">
    <a href="index.html">All {TOTAL} names</a>
    <a href="electronic.html"{' class="active"' if active_nav == 'elec' else ''}>Electronic</a>
    <a href="soul-jazz-afro.html"{' class="active"' if active_nav == 'sj' else ''}>Soul / Jazz / Hip-hop</a>
  </nav>

  <input class="searchbox" id="search" type="search" autocomplete="off"
         aria-label="Search by artist name" placeholder="Search an artist name">

  <div class="chipgroup">
    <span class="chiplabel">Day</span>
    <div class="chips">{day_chips_html()}</div>
  </div>
  <div class="chipgroup">
    <span class="chiplabel">Sound</span>
    <div class="chips">{chips_html(catmap)}</div>
  </div>
  <div class="chipgroup">
    <span class="chiplabel">Stage</span>
    <div class="chips">{stage_chips_html(items)}</div>
  </div>

  <div class="tally">
    <span id="tally"></span>
    <button type="button" class="btn-clear" id="clearFilters" hidden>Clear filters</button>
  </div>

  <div class="grid">
{rows}
  </div>
  <p class="empty" id="emptyMsg" hidden>No sets match that. Clear a filter, or search a different name.</p>

  <p class="note">{NOTE}</p>
  <footer class="credit">{FOOTER}</footer>
</div>
<script src="app.js"></script>
</body>
</html>'''

DAY_FULL = {'Thu': 'Thursday 20 Aug', 'Fri': 'Friday 21 Aug',
            'Sat': 'Saturday 22 Aug', 'Sun': 'Sunday 23 Aug'}

def paragraphs(text, target=380):
    """The blurbs arrive as one block. Break them up so they can be read."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    out, buf = [], ''
    for s in sentences:
        buf = f'{buf} {s}'.strip()
        if len(buf) >= target:
            out.append(buf)
            buf = ''
    if buf:
        # a short tail reads better joined to the previous paragraph
        if out and len(buf) < 120:
            out[-1] += ' ' + buf
        else:
            out.append(buf)
    return out

def artist_page(name, tag, day, time, stage, list_page, list_label):
    """One page per artist: the festival's own blurb, and every set they play."""
    bio, sources = bio_for(name)
    sets = official_sets_for(name, day, time, stage)
    ours = (day, start_minutes(time.partition('-')[0]))

    if sets:
        rows = ''
        for r in sets:
            listed = (r['day'], start_minutes(r['start'])) == ours
            billing = '' if name_tokens(r['artist']) == name_tokens(name) else \
                      f'<span class="billed">billed as {esc(r["artist"])}</span>'
            rows += f'''<li class="gig{' gig--ours' if listed else ''}">
          <span class="gig-when">{esc(DAY_FULL.get(r['day'], r['day']))}</span>
          <span class="gig-time">{esc(r['start'])}&#8211;{esc(r['end'])}</span>
          <span class="gig-stage">{esc(r['stage'])}</span>
          {billing}
        </li>'''
        plural = 'set' if len(sets) == 1 else 'sets'
        playing = f'''<h2 class="side-head">{len(sets)} {plural} at the festival</h2>
        <ol class="gigs">{rows}</ol>'''
        if len(sets) > 1:
            playing += ('<p class="side-note">The list pages show one slot each, '
                        'so the others are only here.</p>')
    else:
        start, _, end = time.partition('-')
        playing = ('<h2 class="side-head">Playing</h2>'
                   f'<ol class="gigs"><li class="gig gig--ours">'
                   f'<span class="gig-when">{esc(DAY_FULL.get(day, day))}</span>'
                   f'<span class="gig-time">{esc(start)}&#8211;{esc(end)}</span>'
                   f'<span class="gig-stage">{esc(stage)}</span></li></ol>')

    verified = VERIFIED.get(re.sub(r'\s*\(.*?\)', '', name).strip())
    links = ''
    if verified:
        links += (f'<a class="btn btn--play" href="{esc(verified)}" target="_blank" rel="noopener">'
                  f'<span aria-hidden="true">&#9654;</span> Play mix</a>')
    links += (f'<a class="btn" href="{esc(sc_search(name))}" target="_blank" rel="noopener">'
              f'Search SoundCloud</a>')
    links += (f'<a class="btn" href="{esc(mc_search(name))}" target="_blank" rel="noopener">'
              f'Search Mixcloud</a>')
    links += (f'<a class="btn" href="{esc(yt_search(name))}" target="_blank" rel="noopener">'
              f'Search YouTube</a>')

    if bio and sources is not None:
        # our own words, so say so and show where the facts came from
        paras = ''.join(f'<p>{esc(p)}</p>' for p in bio.split('\n\n') if p.strip())
        cited = ', '.join(f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'
                          for label, url in sources)
        bio_html = f'''<div class="bio">{paras}
        <p class="bio-source">Written for this site, not by the festival.
        {'Sources: ' + cited + '.' if cited else ''}</p>
      </div>'''
    elif bio:
        paras = ''.join(f'<p>{esc(p)}</p>' for p in paragraphs(bio))
        bio_html = f'''<div class="bio">{paras or f'<p>{esc(bio)}</p>'}
        <p class="bio-source">Blurb from the festival's own listing at
        <a href="https://weoutherefestival.com/set-times/" target="_blank" rel="noopener">weoutherefestival.com</a>.</p>
      </div>'''
    else:
        bio_html = ('<div class="bio"><p class="bio-none">The festival has not published a blurb '
                    'for this one. The search links are the quickest way to hear what they do.</p></div>')

    desc = f'{name} at We Out Here 2026: {tag}, {DAY_FULL.get(day, day)}, {time}, {stage}.'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(name)} &mdash; We Out Here: Do Your Own Research</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(name)} &mdash; We Out Here 2026">
<meta property="og:description" content="{esc(desc)}">
{FONTS}
<link rel="stylesheet" href="../style.css">
</head>
<body>
{THEME_BOOT}
<div class="wrap">
  <header class="masthead masthead--inner">
    <div>
      <p class="eyebrow">{esc(tag)}</p>
      <h1 class="wordmark">{esc(name)}</h1>
    </div>
    <button type="button" class="toggle-btn" id="toggleTheme">Day / night</button>
  </header>

  <nav class="pagenav">
    <a href="../index.html">All {TOTAL} names</a>
    <a href="../{list_page}">Back to {list_label}</a>
  </nav>

  <div class="artist">
    {bio_html}
    <aside class="side">
      {playing}
      <div class="set-links">{links}</div>
    </aside>
  </div>

  <footer class="credit">{FOOTER}</footer>
</div>
<script src="../app.js"></script>
</body>
</html>'''

elec_page = build_page(
    'Electronic',
    'Dub, dubstep, techno, house, electro, garage and drum &amp; bass, across all four days.',
    ELECTRONIC, ELEC_CATS, 'elec',
)
sj_page = build_page(
    'Soul, Jazz &amp; Hip-hop',
    'Live bands, jazz, soul, hip-hop and global sounds: the other half of the bill.',
    SOUL_JAZZ, SJ_CATS, 'sj',
)

index_desc = (f'All {TOTAL} acts at We Out Here 2026, sorted into electronic and soul/jazz/afrobeat, '
              'each with a mix to listen to before you decide.')

index_page = f'''<!DOCTYPE html>
<html lang="en">
<head>
{head('We Out Here: Do Your Own Research', index_desc)}
</head>
<body>
{THEME_BOOT}
<div class="wrap">
  <div class="hero">
    <header class="masthead">
      <div>
        <p class="eyebrow">20&#8211;23 Aug 2026 &middot; Wimborne St Giles, Dorset</p>
        <h1 class="wordmark">We Out Here<span class="research">Do your own research</span></h1>
      </div>
      <button type="button" class="toggle-btn" id="toggleTheme">Day / night</button>
    </header>

    <p class="standfirst">
      <b>{len(ELECTRONIC) + len(SOUL_JAZZ)} names on the bill.</b>
      Maybe eight of them are going to be your weekend. Listen first, then pick,
      so you are not stood at the wrong stage at midnight.
    </p>
    <p class="standfirst-sub">
      Every act below links out to a mix or a search. Pick any name to jump straight to its set time,
      or open a list and filter by day and sound.
    </p>
  </div>

  <div class="wall-head">
    <span>The whole bill, A to Z</span>
    <span>Pick a name for its set time</span>
  </div>
  <div class="wall">{wall_html()}</div>

  <div class="lists">
    <a class="list-tile" href="electronic.html">
      <span class="list-count">{len(ELECTRONIC)} sets</span>
      <h2>Electronic</h2>
      <p>Dub and dubstep, techno, house, electro, garage, drum &amp; bass and everything
         next door to them.</p>
    </a>
    <a class="list-tile" href="soul-jazz-afro.html">
      <span class="list-count">{len(SOUL_JAZZ)} sets</span>
      <h2>Soul, Jazz &amp; Hip-hop</h2>
      <p>Live bands, jazz, soul, hip-hop and global sounds, which is most of what happens
         before dark.</p>
    </a>
  </div>

  <p class="note">{NOTE}</p>
  <footer class="credit">{FOOTER}</footer>
</div>
<script src="app.js"></script>
</body>
</html>'''

os.makedirs('artists', exist_ok=True)
written, multi = set(), 0
for items, list_page, list_label in ((ELECTRONIC, 'electronic.html', 'Electronic'),
                                     (SOUL_JAZZ, 'soul-jazz-afro.html', 'Soul / Jazz / Hip-hop')):
    for name, tag, day, time, stage in items:
        path = os.path.join('artists', f'{slug(name)}.html')
        if path in written:
            continue
        with open(path, 'w') as f:
            f.write(artist_page(name, tag, day, time, stage, list_page, list_label))
        written.add(path)
        if len(official_sets_for(name, day, time, stage)) > 1:
            multi += 1

# drop pages for artists that are no longer in data.py
for stale in set(os.listdir('artists')) - {os.path.basename(p) for p in written}:
    if stale.endswith('.html'):
        os.remove(os.path.join('artists', stale))

with open('style.css', 'w') as f: f.write(CSS)
with open('app.js', 'w') as f: f.write(JS)
with open('electronic.html', 'w') as f: f.write(elec_page)
with open('soul-jazz-afro.html', 'w') as f: f.write(sj_page)
with open('index.html', 'w') as f: f.write(index_page)

print(f"Artist pages: {len(written)} ({multi} play more than one set)")
print(f"Electronic: {len(ELECTRONIC)} sets")
print(f"Soul/Jazz:  {len(SOUL_JAZZ)} sets")
print(f"Featured mixes: {len(VERIFIED)}")
print("Built: index.html, electronic.html, soul-jazz-afro.html, style.css, app.js")
