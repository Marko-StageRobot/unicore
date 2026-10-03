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


# Wrap up the levels and fire them across,
# straight to the gateway, the pixel-paint boss.
def send_test_universe(sock, universe, slots, sequence):
    packet = sacn.build_data_packet(TEST_CID, "We Tested It Once", 100, sequence, universe, slots)
    net.send_packet(sock, packet, universe, LOCALHOST, GATEWAY_PORT)


# Whatever comes back we keep only the last,
# the newest is truest, forget what has passed.
def collect_output(sock, results):
    while True:
        packet = net.receive_packet(sock)
        if packet is None:
            return results
        parsed = sacn.parse_data_packet(packet)
        if parsed is not None:
            results[parsed[0]] = parsed[1]


# Send both of the patterns and listen for more,
# for as many seconds as we have in store.
def run_traffic(patterns, seconds):
    sender = net.make_sending_socket()
    listener = net.make_listening_socket([], NODE_PORT)
    results = {}
    sequence = 0
    deadline = time.time() + seconds
    while time.time() < deadline:
        for universe, slots in patterns.items():
            send_test_universe(sender, universe, slots, sequence)
        collect_output(listener, results)
        sequence = (sequence + 1) & 0xFF
        time.sleep(0.025)
    return results


# Subtract what came back from the thing that was sent,
# the vibes are left out, as was always the intent.
def measure_error(sent, received):
    sent_levels = np.frombuffer(sent, dtype=np.uint8)[:510].astype(int)
    received_levels = np.frombuffer(received, dtype=np.uint8)[:510].astype(int)
    return np.abs(sent_levels - received_levels)


# The mean and the worst and how many were right,
# three little numbers to read in the night.
def describe_error(label, error):
    exact = 100.0 * (error == 0).mean()
    return "%s: mean error %.1f, worst %d, exact %.0f%%" % (label, error.mean(), error.max(), exact)
