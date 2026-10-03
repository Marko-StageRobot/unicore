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
