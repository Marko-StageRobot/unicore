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
