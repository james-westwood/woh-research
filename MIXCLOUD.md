# Task: find the best mix per act for The Grove and Rhythm Corner, 20:00 onwards

Handed off from a Claude Code session. Everything below is already verified, so
please do not re-derive it. The festival starts 20 Aug 2026, so this is urgent.

## What to produce

For each of the 21 acts listed below, find the best (ideally most popular) full
DJ set or mix for that artist on **Mixcloud** and on **SoundCloud**, and add it
to the `VERIFIED` dict in `data.py`:

    VERIFIED = {
        'Artist Name': 'https://soundcloud.com/... or mixcloud url',
    }

`VERIFIED` keys are matched against the artist name with any parenthetical
stripped, so use `'Blawan'` not `'Blawan (Live)'`. A key that is present renders
a marigold "Play mix" button on the list row and the artist page. Then run
`python3 build.py`. Do not edit the generated .html files.

If you want to store both a SoundCloud and a Mixcloud link per artist, that
needs a small change to `build.py` (`set_html` and `artist_page` both read
`VERIFIED`); a second dict such as `VERIFIED_MIXCLOUD` is fine, but keep
`build.py` offline, it must never fetch at build time.

## Verified findings, do not repeat this work

**Mixcloud has no linkable web search.** Confirmed by request and by the
official docs at https://www.mixcloud.com/developers/ :

- `https://www.mixcloud.com/search/?q=X` and `/search?q=X` both 301 to the
  Mixcloud homepage and discard the query.
- `https://www.mixcloud.com/search/cloudcasts/?q=X` answers HTTP 200 but renders
  Mixcloud's own "Page Not Found" screen client-side. It looked fine to curl,
  which is why it briefly shipped. It is not usable.
- Search is an **API** endpoint, not a web route:
  `https://api.mixcloud.com/search/?q=party+time&type=cloudcast`
  `type` must be one of `cloudcast`, `user`, `tag`. No API key needed.

So the only honest Mixcloud link is a direct URL to a specific cloudcast. Use
the API to find one, then put the returned `url` field in `data.py`.

**Two traps in the Mixcloud API:**

1. `play_count` is usually `0`, so you cannot rank by popularity for most
   artists. Do not assume 0 plays means unpopular.
2. Relevance is bad and will produce wrong links if you take the top hit.
   Searching `Scientist` (the dub engineer, playing The Bowl) returns
   "THE BLAST OFF 3 - THE ROCK-IT! SCIENTISTS" with 19,325 plays as the top
   result. It is a different artist entirely.

   Guard against this: require the artist's name tokens to match as whole words
   in either the cloudcast `name` or the uploader (`user.name` /
   `user.username`), and prefer cloudcasts uploaded by the artist themselves or
   by a known radio/label account (NTS, Rinse, Worldwide FM, Crack, Dekmantel,
   Resident Advisor, Mixmag, Balamii, Kiosk Radio, Tru Thoughts).

   **A wrong mix is worse than no mix.** If nothing matches confidently, skip
   that artist and say so.

**SoundCloud has no public search API.** `soundcloud.com/search?q=` works on the
web but needs a `client_id` for api-v2. Options: parse the `__sc_hydration`
JSON blob embedded in a fetched search or profile page, or find the artist's
profile and take their most played set. Note the SoundCloud Android app hijacks
all soundcloud.com links (all three hosts publish app-links for
`com.soundcloud.android`), which is a separate known issue and not yours to fix.

## Checks that must still pass when you are done

    python3 verify.py     # must print "disagree: 0" and "not in official: 0"
    python3 build.py      # regenerates the site and the artists/ pages

Every URL you add must return HTTP 200. There is a working example of a link
check in the git history. 23 mixes are already in `VERIFIED` and all 23 resolve;
do not break them.

## The 21 acts, 20:00 onwards

Acts marked HAS MIX already have one; you may improve it if you find something
clearly better, but the existing 23 all work.

### The Grove
- Thu 20:30-22:00  Ehua                       Afro-house              HAS MIX
- Thu 22:00-23:00  Lone (Live)                House / Techno
- Thu 23:00-00:00  Barker (Live)              Techno                  HAS MIX
- Fri 00:30-02:30  Kenny Dope                 House
- Sat 20:00-22:00  I-Sha                      Experimental electronic HAS MIX
- Sat 22:00-23:00  Shackleton (Live)          Dub-techno              HAS MIX
- Sat 23:00-01:00  re:ni                      Techno                  HAS MIX
- Sat 01:00-02:00  Blawan (Live)               Techno                 HAS MIX
- Sat 02:00-04:00  Nono Gigsta                Genre-warping           HAS MIX
- Sun 20:30-22:00  Bryan Gee (Old Skool Set)  Jungle / Drum & Bass
- Sun 22:00-23:00  Mantra                     Jungle / Drum & Bass
- Sun 23:00-00:00  dBridge                    Drum & Bass / Halftime

### Rhythm Corner
- Thu 20:30-22:30  Juls                       Afrobeats / Highlife    HAS MIX
- Thu 22:30-00:00  Jamz Supernova             Broken Beat / Global bass
- Fri 20:30-23:00  Tama Sumo & Lakuti         House / Techno
- Fri 23:00-01:00  Palms Trax                 House
- Fri 01:00-04:00  Luke Una                   House / Balearic
- Sat 21:00-22:30  Silva Snipa                Jungle / Drum & Bass    HAS MIX
- Sat 22:30-00:00  Alix Perez ft SP:MC        Drum & Bass             HAS MIX
- Sat 00:00-02:00  Calibre ft SP:MC           Drum & Bass             HAS MIX
- Sat 02:00-04:00  Ivy Lab                    Bass / Halftime         HAS MIX

Priority is the 9 with no mix yet: Lone, Kenny Dope, Bryan Gee, Mantra,
dBridge, Jamz Supernova, Tama Sumo & Lakuti, Palms Trax, Luke Una.
