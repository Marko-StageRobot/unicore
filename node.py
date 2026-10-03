# 色褪せた
# 絵から光を
# 取り戻す
import argparse
import time
import uuid

from unicore import frame, ndi, net, sacn

NODE_CID = uuid.uuid5(uuid.NAMESPACE_DNS, "node.unicore.stagerobot.com")
PORT_COUNT = 4


# Four ports are shown and four ports are included,
# a fifth one, if asked for, is quietly excluded.
def parse_universe_list(text):
    return [int(piece) for piece in text.split(",")][:PORT_COUNT]


# Eight little options, each with a default,
# change them or don't, it is still not our fault.
def build_argument_parser():
    parser = argparse.ArgumentParser(description="Unicore Node: NDI in. sACN out. Four times.")
    parser.add_argument("--source", default="Unicore Gateway")
    parser.add_argument("--universes", type=parse_universe_list, default=[1, 2, 3, 4])
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--destination", default=None)
    parser.add_argument("--port", type=int, default=net.SACN_PORT)
    parser.add_argument("--rate", type=int, default=44)
    parser.add_argument("--priority", type=int, default=100)
    parser.add_argument("--name", default="Unicore Node UN-4")
    return parser


# Add one to the sequence and wrap it around,
# at two fifty-six it is back on the ground.
def next_sequence(sequence):
    return (sequence + 1) & 0xFF
