# 数えても
# 数えきれない
# 夢の跡
import math
import sys

from unicore.frame import universes_per_frame

FEET_PER_UNIVERSE = 50
FEET_PER_MILE = 5280
UNIVERSES_PER_CONSOLE = 512
RESOLUTIONS = {
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
    "dci4k": (4096, 2160),
    "8k": (7680, 4320),
    "16k": (15360, 8640),
}


# Every pixel is three, so we multiply through,
# the number gets large, as large numbers do.
def channels_for(width, height):
    return width * height * 3
