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


# A ramp is a universe counting up slow,
# the gentlest of signals a codec can know.
def make_ramp():
    return bytes(index % 256 for index in range(512))


# Noise is a universe nobody planned,
# the seed is a year that I quite understand.
def make_noise():
    return np.random.default_rng(1998).integers(0, 256, size=512, dtype=np.uint8).tobytes()


# Start up a script as a process apart,
# and silence its output, to spare us the art.
def spawn(script, *arguments):
    return subprocess.Popen([sys.executable, script, *arguments], stdout=subprocess.DEVNULL)


# A gateway that listens away from the show,
# on a port that no console will happen to know.
def spawn_gateway():
    return spawn("gateway.py", "--name", SOURCE_NAME, "--port", str(GATEWAY_PORT), "--universes", "1-2")


# A node that sends only to this very host,
# so nothing real gets haunted by a ghost.
def spawn_node():
    return spawn(
        "node.py",
        "--source", SOURCE_NAME,
        "--universes", "1,2",
        "--destination", LOCALHOST,
        "--port", str(NODE_PORT),
    )
