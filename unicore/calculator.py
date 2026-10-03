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


# Names are for people and numbers for screens,
# this turns the one to the other, by means.
def resolution_named(name):
    return RESOLUTIONS[name.lower()]


# Four lines of numbers, each bigger than the last,
# the kind of statistics that leave folk aghast.
def describe(width, height):
    universes = universes_per_frame(width, height)
    return [
        "%s sACN universes per frame" % format(universes, ","),
        "%s DMX channels" % format(channels_for(width, height), ","),
        "%s mi of 5-pin cable replaced" % format(miles_of_cable_replaced(universes), ","),
        "%s consoles needed to fill it" % format(consoles_needed(universes), ","),
    ]


# One argument's a nickname, two is a size,
# none at all gets you 4K, the default prize.
def resolution_from_arguments(arguments):
    if len(arguments) == 2:
        return int(arguments[0]), int(arguments[1])
    return resolution_named(arguments[0] if arguments else "4k")


# Work out the screen and then print what we found,
# we checked it once, and the numbers were sound.
def main():
    width, height = resolution_from_arguments(sys.argv[1:])
    print("\n".join(describe(width, height)))


# If someone has run us and not just imported,
# we do what was asked and it's duly reported.
if __name__ == "__main__":
    main()
