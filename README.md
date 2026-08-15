# We Out Here: Do Your Own Research

A static site listing every act at We Out Here 2026 (20–23 August, Wimborne St Giles), with a
link out to a mix for each one. Built so you can decide who you actually want to see before the
weekend starts, rather than reading a name on a stage and hoping.

**Live: https://james-westwood.github.io/woh-research/**

The lineup is split into two lists, because in practice you plan around them separately:

- **Electronic** (87 sets): dub and dubstep, techno, house, electro, garage, drum & bass.
- **Soul, Jazz & Afrobeat** (56 sets): live bands, jazz, soul, hip-hop and global sounds.

Both lists run in chronological order, and filter by day, by sound and by stage, plus a search
by name. Sounds and stages are additive, so selecting Techno and House shows both. Every set
shows its time, stage and genre.

Note that the running order treats a festival day as ending at 06:00, not at midnight. A set
listed at 01:00 on Saturday is the small hours at the end of Saturday night, so it sorts after
the Saturday evening sets rather than before the Saturday afternoon ones. Saturday at The Grove
comes out as I-Sha 20:00, Shackleton 22:00, re:ni 23:00, Blawan 01:00, Nono Gigsta 02:00, which
is how you would actually stand there and watch it.

Nineteen artists have a specific mix picked out and marked "Play mix"; the rest link to a
SoundCloud and Mixcloud search so you can dig yourself. The landing page lists all 143 names
alphabetically, and picking one jumps straight to its set time.

## Building it

No dependencies and no build tooling. `data.py` holds the lineup, `build.py` writes the HTML,
CSS and JS:

```bash
python3 build.py
```

That regenerates `index.html`, `electronic.html`, `soul-jazz-afro.html`, `style.css` and
`app.js`. Edit `data.py` or `build.py`, never the generated files, or your changes get
overwritten on the next build.

## Coverage and caveats

**This is a shortlist, not the full programme.** The official schedule has 565 sets across 18
stages. This site lists 143 of them. Four stages are missing entirely (Once In A Blue Moon,
Worldwide FM presents: WOH Radio, Love-Serve Bar, Passenger Presents: Ground Tempo) and the
stages that are included are not complete either, so the festival's own set-times page stays the
authority on where to stand. Where an artist plays more than once, one slot is listed.

## Checking the data

`verify.py` fetches the official set-times page, parses all 565 listings out of it, and diffs
them against `data.py`:

```bash
python3 verify.py                 # fetch and check
python3 verify.py --cache page.html   # check against a saved copy
```

It exits non-zero if anything disagrees, and reports how much of the programme is uncovered.
Matching is done on day plus stage plus start time rather than on artist name, because the
festival renames compound sets freely: our "Nightmares on Wax b2b Trojan Sound System b2b Daddy
G" appears officially as "TROJAN SOUND SYSTEM B2B NIGHTMARES ON WAX B2B DADDY G WITH VERY SPECIAL
GUESTS: ...".

Running this on 15 August 2026 caught seven wrong entries, since fixed: V.I.V.E.K out by 90
minutes, Introspekt on the wrong day, Rogê on the wrong stage, and start or end times out on
Josey Rebelle, Plumm, Jamz Supernova and Pariah. All 143 now agree with the official listing.

Built for the group chats. This is not official festival material and has nothing to do with the
organisers.
