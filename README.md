# We Out Here: Do Your Own Research

A static site listing every act at We Out Here 2026 (20–23 August, Wimborne St Giles), with a
link out to a mix for each one. Built so you can decide who you actually want to see before the
weekend starts, rather than reading a name on a stage and hoping.

**Live: https://james-westwood.github.io/woh-research/**

The lineup is split into two lists, because in practice you plan around them separately:

- **Electronic** (86 sets): dub and dubstep, techno, house, electro, garage, drum & bass.
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
SoundCloud and Mixcloud search so you can dig yourself. The landing page lists all 142 names
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

Times come from the We Out Here Clashfinder as of 15 August 2026, so recheck the festival app
closer to the day. Where an artist plays more than once, one representative slot is listed.

The site covers the officially announced lineup plus a handful of extras worth knowing about
(I-Sha, Silva Snipa, Introspekt, rRoxymore, Ivy Lab, Ceephax Acid Crew, and dub and house
regulars like Mad Professor and DJ Lag). It does not cover every name on the smaller record-shop
and community stages, where there are another 100+ local selectors on the festival's own
set-times app.

Built for the group chats. This is not official festival material and has nothing to do with the
organisers.
