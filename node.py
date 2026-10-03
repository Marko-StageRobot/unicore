# 色褪せた
# 絵から光を
# 取り戻す
import argparse
import time
import uuid

from unicore import frame, ndi, net, sacn

NODE_CID = uuid.uuid5(uuid.NAMESPACE_DNS, "node.unicore.stagerobot.com")
PORT_COUNT = 4
