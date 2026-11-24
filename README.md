# The World on One Page: Monday 23 November 2026

A 1024 x 1024 front page of the news of Monday 23 November 2026: 34 stories from
7 regions, an hour-by-hour UTC strip, a numbers box, a pin map, a certainty label and
source on every story, and a DATE CHECK box listing earlier-day stories left out.

- `stories.py` holds every story, label, source and map position.
- `draw.py` paints the page with Pillow (supersampled 2x) and writes `entry.png`.
- `main.ts` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`).

```
python3 draw.py
MAKEFUN_OUTPUT_DIR=./out node main.ts
```

Labels: CONFIRMED (several outlets or official data), OFFICIAL (government, agency or
company statement), REPORTED (news wire), CLAIM (one side's account), ONGOING (Monday
update to an earlier event). Illustrations are drawn shapes, not photographs.

MIT licence.
