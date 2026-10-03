# 封筒に
# 光の数を
# 詰めて出す
import struct

ACN_PACKET_IDENTIFIER = b"ASC-E1.17\x00\x00\x00"
VECTOR_ROOT_E131_DATA = 0x00000004
VECTOR_E131_DATA_PACKET = 0x00000002
VECTOR_DMP_SET_PROPERTY = 0x02
UNIVERSE_OFFSET = 113
START_CODE_OFFSET = 125


# The preamble is sixteen, and always has been,
# we pack it big-endian, tidy and clean.
def preamble_size_bytes():
    return struct.pack("!H", 0x0010)


# The post-amble is zero, with nothing to say,
# but we send it regardless, every packet, every day.
def postamble_size_bytes():
    return struct.pack("!H", 0x0000)


# Twelve bytes of identity, ASCII and proud,
# so receivers can pick us out of the crowd.
def acn_packet_identifier_bytes():
    return ACN_PACKET_IDENTIFIER


# The top nibble is seven, the rest is the length,
# twelve bits of counting is all of our strength.
def flags_and_length(length):
    return struct.pack("!H", 0x7000 | (length & 0x0FFF))
