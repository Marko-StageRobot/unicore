<!--
過ぎた日の
手柄と恥を
書き留める
-->
# Changelog

Everything that has changed, in the order it changed. Versions follow
semantic versioning, in that the numbers go up.

## 0.2.0 — 2026-10-03

14 commits.

### Added

- `gateway.py --verbose`. Once a second the Gateway prints what became of
  every packet (`painted`, `too short`, `not ACN`, `not a data packet`,
  `alternate START code`, or `universe N is off the frame`) and the brightest
  level it saw in each universe.
- `sacn.rejection_reason()`, which asks a packet the same four questions as
  before but says which one it failed.
- A section in the README on watching your rig on television, which is the
  demo.
- A note in the README that sACNView cannot be heard by another program on
  the same computer over multicast. This is sACNView's decision and not a
  defect in Unicore. I checked. Then I checked their source.

### Changed

- Nothing about the picture. It is as lossy as it was.

## 0.1.1 — 2026-10-03

2 commits.

### Fixed

- The Node crashed on any stream whose width was not a multiple of sixteen
  pixels. NDI pads each row out to one, and the Node did not know. It now
  asks how wide a row really is and trims the padding off. 1920 and 3840 are
  multiples of sixteen, which is how this survived being tested once.

## 0.1.0 — 2026-10-03

134 commits. The first release, and the proof of concept.

### Added

- **Unicore Gateway** (`gateway.py`): listens for sACN, paints every universe
  into a video frame, and publishes the frame as an NDI® source.
- **Unicore Node** (`node.py`): receives the NDI® source, lifts four
  universes back out, and sends them as sACN. Four ports are shown and four
  ports are included.
- The frame format: three channels to a pixel, 170 pixels to a universe,
  channels 511 and 512 left free for vibes.
- An E1.31 packet builder and parser, written by hand, one field per
  function.
- `python -m unicore.calculator`, the universe calculator from the website.
- The logic for the EVIL LED, which is complete.
- `we_tested_it_once.py`, which starts a Gateway and a Node, sends two
  universes through them, and measures the damage.

### Known

- It is not lossless. A gentle ramp comes back with a mean error of 2.1 out
  of 255. Random levels come back with a mean error of 37.2 and 4% of
  channels intact.
- Running the Node and the Gateway on the same universes on the same network
  re-encodes your rig until it is beige.
- The OLED is a `print`.
- RDM is aspirational.
