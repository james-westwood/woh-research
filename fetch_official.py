"""Snapshot the official schedule and artist bios into JSON for build.py.

    python3 fetch_official.py

Writes official_schedule.json (every set on the official timetable) and
artist_bios.json (the festival's own artist blurbs). Both are committed so that
build.py never needs the network; rerun this when the festival updates things,
then run verify.py and build.py.

The bios come from the same AJAX endpoint the site's own artist modal uses.
Only artists the schedule links a modal to have one, which is about 200 of them.
"""
import collections
import html as htmllib
import json
import re
import time
import urllib.parse
import urllib.request

import verify  # reuse the set-times parser so there is only one copy of it

AJAX = 'https://weoutherefestival.com/wp-admin/admin-ajax.php'
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
HEADERS = {'User-Agent': UA, 'X-Requested-With': 'XMLHttpRequest'}


def get(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60
    ).read().decode('utf-8', 'replace')


def fetch_bio(artist_id):
    body = urllib.parse.urlencode({
        'action': 'plotLoadTemplatePart',
        'templatePart': 'parts/artist-biog',
        'data[artistId]': artist_id,
    }).encode()
    payload = json.load(urllib.request.urlopen(
        urllib.request.Request(AJAX, data=body, headers=HEADERS), timeout=60))
    raw = payload.get('html') or ''
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', raw, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', htmllib.unescape(text)).strip()
    return text


def main():
    doc = get(verify.URL)

    schedule = verify.parse(doc)
    if len(schedule) < 400:
        raise SystemExit(f'only parsed {len(schedule)} sets; the page layout probably changed')
    json.dump(schedule, open('official_schedule.json', 'w'), indent=1, ensure_ascii=False)
    print(f'official_schedule.json: {len(schedule)} sets, '
          f"{len(set(r['stage'] for r in schedule))} stages, "
          f"{dict(collections.Counter(r['day'] for r in schedule))}")

    ids = {}
    for m in re.finditer(r'data-plot-modal-data-artist-id="(\d+)"[^>]*>([^<]{1,120})<', doc):
        name = htmllib.unescape(re.sub(r'\s+', ' ', m.group(2))).strip()
        if name:
            ids.setdefault(m.group(1), name)

    bios = {}
    for i, (artist_id, name) in enumerate(sorted(ids.items(), key=lambda kv: kv[1].lower()), 1):
        try:
            text = fetch_bio(artist_id)
        except Exception as exc:  # a missing bio should not sink the whole run
            print(f'  ! {name}: {exc}')
            continue
        # the blurb repeats the artist name first; drop it so it is not shown twice
        if text.lower().startswith(name.lower()):
            text = text[len(name):].strip(' -–—:')
        if text:
            bios[name] = text
        if i % 50 == 0:
            print(f'  bios {i}/{len(ids)}')
        time.sleep(0.25)

    json.dump(bios, open('artist_bios.json', 'w'), indent=1, ensure_ascii=False)
    print(f'artist_bios.json: {len(bios)} bios, '
          f'{sum(len(v) for v in bios.values()) // max(1, len(bios))} chars average')


if __name__ == '__main__':
    main()
