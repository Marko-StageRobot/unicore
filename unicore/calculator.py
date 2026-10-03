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


# At fifty feet each, laid out end to end,
# that's how many miles you no longer need spend.
def miles_of_cable_replaced(universes):
    return universes * FEET_PER_UNIVERSE // FEET_PER_MILE


# A console does five-twelve, if it's feeling brave,
# round up for how many consoles you'd crave.
def consoles_needed(universes):
    return math.ceil(universes / UNIVERSES_PER_CONSOLE)
