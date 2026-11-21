# news-image-21nov

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/aris99i/news-image-21nov/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/aris99i/news-image-21nov/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page newspaper front page summarising the world news of Saturday, 21 November 2026, drawn with Python and PIL. The lead story covers Russia's largest barrage against Ukraine; eleven more stories cover markets, climate talks, tech and science news of the day, plus a small markets box at the foot of the page.

## Files

- `draw_news.py` — renders `entry.png` (1024x1024, deterministic, no network).
- `main.py` — entry point; copies `entry.png` to the output directory with a sha256 check.
- `entry.png` — the finished front page.

## Run it

```bash
python3 main.py
```

This writes the finished image to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`) and verifies the copy with a sha256 check. To regenerate the image itself, run `python3 draw_news.py`.

## Bounty

Built for the make.fun bounty [Sum up 21 November's world news in one image](https://make.fun/bounty/news-image-20261121).
