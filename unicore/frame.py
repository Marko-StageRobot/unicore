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


# Five-eleven and five-twelve are left free for vibes,
# exactly as the marketing page describes.
def discard_vibes(slots):
    return bytes(slots[:SLOTS_PER_UNIVERSE])


# A universe sent short gets padded with dark,
# so every one of them hits the five-ten mark.
def pad_slots(slots):
    return slots.ljust(SLOTS_PER_UNIVERSE, b"\x00")


# Three channels a pixel: red, green, then blue,
# one-seventy rows, with three columns through.
def slots_to_pixels(slots):
    padded = pad_slots(discard_vibes(slots))
    return np.frombuffer(padded, dtype=np.uint8).reshape(PIXELS_PER_UNIVERSE, 3)


# Run the trick backwards, from colour to level,
# what the codec did to it is between it and the devil.
def pixels_to_slots(pixels):
    return np.ascontiguousarray(pixels, dtype=np.uint8).tobytes()


# The two missing channels come back as a nought,
# vibes cannot travel, or so I was taught.
def restore_vibes(slots):
    return slots.ljust(SLOTS_PER_DMX_UNIVERSE, b"\x00")


# Find where it lives and then colour it in,
# a universe painted, as thin as a pin.
def paint_universe(frame, universe, slots):
    if not universe_fits(frame, universe):
        return False
    start = first_pixel_of(universe)
    flat_pixels(frame)[start:start + PIXELS_PER_UNIVERSE, :3] = slots_to_pixels(slots)
    return True


# Find where it lived and then peel it away,
# five hundred twelve slots to send on their way.
def unpaint_universe(frame, universe):
    if not universe_fits(frame, universe):
        return None
    start = first_pixel_of(universe)
    pixels = flat_pixels(frame)[start:start + PIXELS_PER_UNIVERSE, :3]
    return restore_vibes(pixels_to_slots(pixels))
