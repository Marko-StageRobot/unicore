<!--
宇宙ごと
一枚の絵に
閉じ込める
-->
# Unicore

sACN over NDI®. Your entire rig, in a single video frame.

This is the proof of concept behind the [Unicore Gateway and Unicore Node](https://stagerobot.com/#unicore).
It is not the shipping firmware. The shipping firmware is more real.

## How it works

Every DMX channel becomes one colour value. Three channels to a pixel, 170
pixels to a universe. That is 510 slots. Channels 511 and 512 are left free
for vibes.

| Screen | Universes |
|---|---|
| 1920 × 1080 | 12,197 |
| 3840 × 2160 | 48,790 |

Universe 1 starts at the top-left pixel. Universe 2 starts 170 pixels later.
It continues like that. You can check the arithmetic with
`python -m unicore.calculator 4k`. We checked it once.

## Running it

```
python -m venv venv && ./venv/bin/pip install -r requirements.txt

./venv/bin/python gateway.py --universes 1-16      # sACN in, NDI out
./venv/bin/python node.py --universes 1,2,3,4      # NDI in, sACN out, four times
```

Point any NDI monitor at `Unicore Gateway UG-1` and your rig appears as
colourful, meaningful static.

**Do not run the Node and the Gateway on the same universes on the same
network.** The Node's output becomes the Gateway's input and your rig is
re-encoded sixty times a second until it is beige. Use `--offset 1000`, or
`--destination`, or a different building.

## Is it lossless

No.

`python we_tested_it_once.py` starts a Gateway and a Node on this machine,
sends two universes through them, and compares what went in with what came
out. On the one occasion we ran it:

| Universe | Mean error | Worst channel | Channels that survived exactly |
|---|---|---|---|
| A gentle ramp | 2.1 of 255 | 58 | 17% |
| Random levels | 37.2 of 255 | 249 | 4% |

NDI subsamples chroma, which means each pixel shares its opinions about
colour with the pixel next to it. In lighting terms: every fixture is
slightly influenced by its neighbour. We are choosing to describe this as
"ambient crosstalk" and to charge for it.

## Things that are not here

- The OLED. It is a `print`.
- The EVIL LED's driver circuit. See `unicore/evil.py` for the logic, which is complete.
- RDM. Aspirational.

## Legal

NDI® is a registered trademark of Vizrt NDI AB, which has not been consulted.
See [ndi.video](https://ndi.video/). This repository contains no NDI SDK
code; it reaches the NDI runtime through [cyndilib](https://github.com/nocarryr/cyndilib).

Read `CONTRIBUTING.md` before you touch anything.
