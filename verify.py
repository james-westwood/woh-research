"""Check data.py against the official We Out Here set times.

    python3 verify.py            # fetch the official page and diff
    python3 verify.py --cache f  # diff against an already-saved copy

Exits non-zero if any of our sets disagree with the official schedule, so this
can be run before a rebuild. It reports three things:

  1. sets whose day/time/stage disagree with the official listing
  2. sets that do not appear in the official schedule at all
  3. how much of the official programme we do not cover (informational)

Matching is done on day + stage + start time first, because the festival
renames compound sets freely (our "Nightmares on Wax b2b Trojan Sound System
b2b Daddy G" is listed officially as "TROJAN SOUND SYSTEM B2B NIGHTMARES ON WAX
B2B DADDY G WITH VERY SPECIAL GUESTS: ..."). Only if a slot cannot be matched
that way do we fall back to comparing names.
"""
import argparse
import collections
import html as htmllib
import re
import sys
import unicodedata
import urllib.request

from data import ELECTRONIC, SOUL_JAZZ

URL = 'https://weoutherefestival.com/set-times/'
DAY_BY_DATE = {'20/08/2026': 'Thu', '21/08/2026': 'Fri', '22/08/2026': 'Sat', '23/08/2026': 'Sun'}
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'


def clean(s):
    return re.sub(r'\s+', ' ', htmllib.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def to24(t):
    m = re.fullmatch(r'(\d{1,2}):(\d{2})(am|pm)', t.strip().lower())
    if not m:
        return None
    h, mi, ap = int(m.group(1)), m.group(2), m.group(3)
    if ap == 'pm' and h != 12:
        h += 12
    if ap == 'am' and h == 12:
        h = 0
    return f'{h:02d}:{mi}'


def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r'\(.*?\)', ' ', s)
    s = re.sub(r'&', ' and ', s)
    s = re.sub(r'\b(live|dj set|b2b|presents|feat|ft|with|the|a)\b', ' ', s)
    return re.sub(r'[^a-z0-9]+', '', s)


def tokens(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return {t for t in re.split(r'[^a-z0-9]+', s) if len(t) > 2}


def parse(doc):
    stage_names = {}
    for m in re.finditer(
            r'data-stage-id="(\d+)"[^>]*>\s*<div class="scheduleCalendar__heading">([^<]+)</div>', doc):
        stage_names[m.group(1)] = clean(m.group(2))

    marks = [(m.group(1), m.start()) for m in re.finditer(
        r'<div\s+class="scheduleCalendarWrap[^"]*"\s+data-schedule-day="([^"]+)"', doc)]
    marks.append((None, len(doc)))

    rows = []
    for (date, start), (_, end) in zip(marks, marks[1:]):
        day = DAY_BY_DATE.get(date)
        if not day:
            continue
        block = doc[start:end]
        cols = list(re.finditer(
            r'<div\s+class="scheduleCalendar__column"\s+data-stage-id="(\d+)"', block))
        bounds = [c.start() for c in cols[1:]] + [len(block)]
        for col, col_end in zip(cols, bounds):
            stage = stage_names.get(col.group(1), 'stage-' + col.group(1))
            for lm in re.finditer(
                    r'scheduleCalendar__performanceTime">([^<]*)</div>\s*<h4>(.*?)</h4>',
                    block[col.start():col_end], re.S):
                artist = clean(lm.group(2))
                tm = re.match(r'\s*(\d{1,2}:\d{2}(?:am|pm))\s*-\s*(\d{1,2}:\d{2}(?:am|pm))',
                              lm.group(1).strip(), re.I)
                if artist and tm:
                    rows.append({'artist': artist, 'day': day, 'stage': stage,
                                 'start': to24(tm.group(1)), 'end': to24(tm.group(2))})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cache', help='read the official page from this file instead of fetching')
    args = ap.parse_args()

    if args.cache:
        doc = open(args.cache, encoding='utf-8', errors='replace').read()
    else:
        req = urllib.request.Request(URL, headers={'User-Agent': UA})
        doc = urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace')

    official = parse(doc)
    if len(official) < 400:
        print(f'ABORT: only parsed {len(official)} official sets; the page layout probably changed.')
        return 2

    ours = [(*x, 'electronic') for x in ELECTRONIC] + [(*x, 'soul-jazz') for x in SOUL_JAZZ]

    by_slot = collections.defaultdict(list)
    by_name = collections.defaultdict(list)
    for r in official:
        by_slot[(r['day'], r['stage'], r['start'])].append(r)
        by_name[norm(r['artist'])].append(r)

    wrong, absent, ok = [], [], 0
    for name, tag, day, time, stage, page in ours:
        start, _, end = time.partition('-')
        slot = by_slot.get((day, stage, start), [])
        # same slot and a shared word in the name: this is our set, whatever it is called
        hit = next((r for r in slot if tokens(r['artist']) & tokens(name)), None)
        if hit:
            if hit['end'] != end:
                wrong.append((name, page, [f"end ours={end} official={hit['end']}"]))
            else:
                ok += 1
            continue

        cands = by_name.get(norm(name), [])
        if not cands:
            for k, v in by_name.items():
                if len(k) >= 6 and (norm(name).startswith(k) or k.startswith(norm(name))):
                    cands = v
                    break
        if not cands:
            absent.append((name, day, time, stage, page))
            continue
        best = min(cands, key=lambda r: (r['day'] != day, r['stage'] != stage, r['start'] != start))
        diff = []
        if best['day'] != day:
            diff.append(f"day ours={day} official={best['day']}")
        if best['stage'] != stage:
            diff.append(f"stage ours={stage!r} official={best['stage']!r}")
        if best['start'] != start:
            diff.append(f"start ours={start} official={best['start']}")
        if best['end'] != end:
            diff.append(f"end ours={end} official={best['end']}")
        wrong.append((name, page, diff)) if diff else None
        if not diff:
            ok += 1

    print(f'ours {len(ours)} sets   official {len(official)} sets / '
          f"{len(set(r['stage'] for r in official))} stages")
    print(f'  agree with official : {ok}')
    print(f'  disagree            : {len(wrong)}')
    print(f'  not in official     : {len(absent)}')

    for name, page, diff in sorted(wrong):
        print(f'\nDISAGREES  {name}  [{page}]')
        for d in diff:
            print(f'    {d}')
    for name, day, time, stage, page in sorted(absent):
        print(f'\nNOT IN OFFICIAL  {name}  {day} {time} {stage}  [{page}]')

    our_names = {norm(n) for n, *_ in ours}
    our_stages = {s for *_, s, _ in ours}
    missing = [r for r in official if norm(r['artist']) not in our_names]
    on_covered = [r for r in missing if r['stage'] in our_stages]
    print(f'\ncoverage: we list {len(ours)} of {len(official)} official sets; '
          f'{len(missing)} absent, {len(on_covered)} of those on stages we already show')

    return 1 if (wrong or absent) else 0


if __name__ == '__main__':
    sys.exit(main())
