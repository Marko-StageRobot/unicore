# 光らぬ灯
# 画素に姿を
# 変えてゆく
import numpy as np

PIXELS_PER_UNIVERSE = 170
SLOTS_PER_UNIVERSE = 510
SLOTS_PER_DMX_UNIVERSE = 512


# Width times height, by one-seventy, floored,
# is how many universes a frame can afford.
def universes_per_frame(width, height):
    return (width * height) // PIXELS_PER_UNIVERSE
