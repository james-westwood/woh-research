import html
import re
from urllib.parse import quote
from data import ELECTRONIC, SOUL_JAZZ, VERIFIED, NOTE

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
    return f"https://www.mixcloud.com/search/?q={quote(base_name(name))}"

DAYS = ['Thu', 'Fri', 'Sat', 'Sun']
DAY_NAMES = {'Thu': 'Thu 20', 'Fri': 'Fri 21', 'Sat': 'Sat 22', 'Sun': 'Sun 23'}

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

    return f'''<article class="set" data-day="{esc(day)}" data-cat="{esc('|'.join(cats))}" data-name="{esc(name.lower())}">
      <div class="clock">
        <span class="clock-start">{esc(start)}</span>
        <span class="clock-end">{esc(end)}</span>
      </div>
      <div class="set-main">
        <h3 class="set-name">{esc(name)}</h3>
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

def day_chips_html():
    return ''.join(
        f'<button type="button" class="chip" data-day-filter="{esc(d)}" aria-pressed="false">{esc(DAY_NAMES[d])}</button>'
        for d in DAYS
    )

def wall_html():
    """Every name on the bill, alphabetical, each deep-linking to its own filtered row."""
    seen = {}
    for items, page in ((ELECTRONIC, 'electronic.html'), (SOUL_JAZZ, 'soul-jazz-afro.html')):
        for name, *_ in items:
            seen.setdefault(name, page)
    names = sorted(seen, key=lambda n: n.lower())
    # Joined on newlines so the browser has somewhere to break the line.
    return '\n'.join(
        f'<a class="wall-name" href="{seen[n]}?q={quote(base_name(n))}">{esc(n)}</a>'
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
  color: var(--ink);
  overflow-wrap: break-word;
}
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

  var activeDay = null;
  var activeCats = [];
  var term = '';

  function apply() {
    var visible = 0;
    sets.forEach(function (el) {
      var cats = el.getAttribute('data-cat').split('|');
      var dayOk = !activeDay || el.getAttribute('data-day') === activeDay;
      // Several sounds per set, so any selected sound matching is enough.
      var catOk = !activeCats.length || cats.some(function (c) { return activeCats.indexOf(c) !== -1; });
      var nameOk = !term || el.getAttribute('data-name').indexOf(term) !== -1;
      var show = dayOk && catOk && nameOk;
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

  search.addEventListener('input', function () {
    term = search.value.trim().toLowerCase();
    apply();
  });

  clearBtn.addEventListener('click', function () {
    activeDay = null;
    activeCats = [];
    term = '';
    search.value = '';
    dayBtns.concat(catBtns).forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
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
    <a href="index.html">All 142 names</a>
    <a href="electronic.html"{' class="active"' if active_nav == 'elec' else ''}>Electronic</a>
    <a href="soul-jazz-afro.html"{' class="active"' if active_nav == 'sj' else ''}>Soul / Jazz / Afrobeat</a>
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

elec_page = build_page(
    'Electronic',
    'Dub, dubstep, techno, house, electro, garage and drum &amp; bass, across all four days.',
    ELECTRONIC, ELEC_CATS, 'elec',
)
sj_page = build_page(
    'Soul, Jazz &amp; Afrobeat',
    'Live bands, jazz, soul, hip-hop and global sounds: the other half of the bill.',
    SOUL_JAZZ, SJ_CATS, 'sj',
)

index_desc = ('All 142 acts at We Out Here 2026, sorted into electronic and soul/jazz/afrobeat, '
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
      <h2>Soul, Jazz &amp; Afrobeat</h2>
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

with open('style.css', 'w') as f: f.write(CSS)
with open('app.js', 'w') as f: f.write(JS)
with open('electronic.html', 'w') as f: f.write(elec_page)
with open('soul-jazz-afro.html', 'w') as f: f.write(sj_page)
with open('index.html', 'w') as f: f.write(index_page)

print(f"Electronic: {len(ELECTRONIC)} sets")
print(f"Soul/Jazz:  {len(SOUL_JAZZ)} sets")
print(f"Featured mixes: {len(VERIFIED)}")
print("Built: index.html, electronic.html, soul-jazz-afro.html, style.css, app.js")
