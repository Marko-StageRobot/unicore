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


# A frame full of nothing, four bytes to a dot,
# red, green and blue, and a fourth that is not.
def blank_frame(width, height):
    return np.zeros((height, width, 4), dtype=np.uint8)


# The fourth byte is padding, it carries no light,
# we set it to full so the frame looks alright.
def fill_padding(frame):
    frame[..., 3] = 255
    return frame
