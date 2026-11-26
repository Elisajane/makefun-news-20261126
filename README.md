[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Elisajane/makefun-news-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Elisajane/makefun-news-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

Entry for the [Sum up 26 November's world news in one image](https://make.fun/bounty/news-image-20261126) bounty on make.fun.

# World News — Thursday, 26 November 2026

A newspaper front page that sums up the world news of Thursday
26 November 2026 in a single image: one lead story, four more in a
grid, and a closing story, all drawn and typeset from scratch.

## The six stories

1. **Cairo tanker fire (lead).** A fuel tanker carrying petroleum
   products overturned on the Greater Cairo Ring Road and burst into
   flames, killing at least 31 people and injuring 21.
2. **Wall Street slides.** The Nasdaq fell almost 4% as investors fled
   artificial-intelligence shares, dragging all three main US indexes
   down.
3. **Taipei welcomes the lowest US tariff rate.** Taiwan said
   Washington's proposed 15% duty puts it in the lowest tier, beside
   Japan, South Korea and the EU; the plan covers 14 economies.
4. **India marks 18 years since the Mumbai attacks.** India remembered
   the 26/11 siege of 2008, in which more than 160 people were killed,
   and marked Constitution Day.
5. **Hera reveals a cratered, tumbling asteroid.** Europe's Hera probe
   sent back the first close views of Dimorphos, the asteroid struck by
   NASA's DART mission in 2022; its face is now a crater as wide as a
   stadium.
6. **Thanksgiving storm batters the US East Coast.** Heavy rain, gusts
   of up to 60 mph and major coastal flooding hit the East Coast on
   Thanksgiving Day, snarling travel for millions.

Every headline and body is phrased in the author's own words.

The six were chosen as the day's most consequential stories, across
regions and fields — a disaster in Egypt, markets and trade in the
United States and Asia, remembrance in India, space science in Europe,
and weather on the US East Coast — and every one of them was first
reported on 26 November 2026.

## How to run

Build the image, then copy it to the output directory:

```sh
python3 build_image.py
python3 main.py
```

`build_image.py` needs Pillow and the DejaVu fonts; it writes
`entry.png` (1024x1024) next to itself. `main.py` uses only the
Python standard library and copies that file to `/output/entry.png`.
To write somewhere else while testing locally, set `OUTPUT_DIR`:

```sh
OUTPUT_DIR=/tmp/out python3 main.py
```

## Determinism

The image is drawn from fixed text and fixed shapes. Nothing is read
from the network, nothing is random, and no time or date is used, so
repeated runs produce byte-identical output. Verified locally: two
separate runs of `main.py` produced identical `entry.png` files with
matching SHA-256 digests.
