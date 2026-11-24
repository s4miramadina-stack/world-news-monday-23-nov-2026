# The World on One Page: Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/s4miramadina-stack/world-news-monday-23-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/s4miramadina-stack/world-news-monday-23-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

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

---

<sub>Entered on [make.fun](https://make.fun/?ref=1cg5hjc5&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
