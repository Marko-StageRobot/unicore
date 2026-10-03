# 門番は
# 全ての声を
# 色にする
import argparse
import time

from unicore import evil, frame, ndi, net, sacn


# A first and a last with a dash in between,
# or only a first, if that's all that is seen.
def parse_universe_range(text):
    first, _dash, last = text.partition("-")
    return list(range(int(first), int(last or first) + 1))


# Six little options, each with a default,
# change them or don't, it is not our fault.
def build_argument_parser():
    parser = argparse.ArgumentParser(description="Unicore Gateway: sACN in. NDI out. Questions later.")
    parser.add_argument("--name", default="Unicore Gateway UG-1")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("--universes", type=parse_universe_range, default=parse_universe_range("1-16"))
    parser.add_argument("--port", type=int, default=net.SACN_PORT)
    return parser


# Parse it, and if it is something we know,
# paint it right into the frame, row by row.
def absorb_packet(canvas, packet):
    parsed = sacn.parse_data_packet(packet)
    if parsed is None:
        return False
    universe, slots = parsed
    return frame.paint_universe(canvas, universe, slots)


# Keep taking packets until there are none,
# then say how many, and that part is done.
def absorb_pending_packets(sock, canvas):
    absorbed = 0
    while True:
        packet = net.receive_packet(sock)
        if packet is None:
            return absorbed
        absorbed += absorb_packet(canvas, packet)


# One over the frame rate is how long to rest,
# sixty a second is sixteen more than requested.
def frame_interval(fps):
    return 1.0 / fps


# The OLED would show this, if we had one to show,
# instead it's a print, as the budget is low.
def announce(args):
    universes = frame.universes_per_frame(args.width, args.height)
    print("%s: %d universes in %dx%d" % (args.name, universes, args.width, args.height), flush=True)


# Redraw the front panel on one single line,
# the fourth light is lit, and the rest may be fine.
def show_front_panel(absorbed):
    print("\r" + evil.render_front_panel(absorbed > 0, True), end="", flush=True)
