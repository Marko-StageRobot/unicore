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


# Blank it, then pad it, and hand it right back,
# a canvas of darkness, expensively black.
def new_frame(width, height):
    return fill_padding(blank_frame(width, height))


# Rows and columns are a human affair,
# we flatten them out to one line, with care.
def flat_pixels(frame):
    return frame.reshape(-1, 4)


# Universe one sits at pixel nought,
# each after that is one-seventy on, as taught.
def first_pixel_of(universe):
    return (universe - 1) * PIXELS_PER_UNIVERSE


# A universe fits if its very last dot
# is inside of the frame, and not if it's not.
def universe_fits(frame, universe):
    if universe < 1:
        return False
    return first_pixel_of(universe) + PIXELS_PER_UNIVERSE <= flat_pixels(frame).shape[0]
