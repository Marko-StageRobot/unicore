# 一度だけ
# 試してみたら
# 美しい
import subprocess
import sys
import time
import uuid

import numpy as np

from unicore import net, sacn

TEST_CID = uuid.uuid5(uuid.NAMESPACE_DNS, "test.unicore.stagerobot.com")
SOURCE_NAME = "Unicore Test Rig"
LOCALHOST = "127.0.0.1"
GATEWAY_PORT = 15568
NODE_PORT = 15569
PATTERN_NAMES = {1: "ramp", 2: "noise"}
