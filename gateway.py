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
