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


# The root layer counts from octet sixteen,
# one hundred and ten, plus the slots in between.
def root_layer_length(slot_count):
    return 110 + slot_count


# The vector says data, the number is four,
# it has never been anything else before.
def root_vector_bytes():
    return struct.pack("!L", VECTOR_ROOT_E131_DATA)


# A CID is a UUID, sixteen bytes wide,
# we take what we're given and pass it inside.
def cid_bytes(cid):
    return cid.bytes


# Six little pieces all joined in a row,
# and that is the root layer, ready to go.
def build_root_layer(cid, slot_count):
    return b"".join([
        preamble_size_bytes(),
        postamble_size_bytes(),
        acn_packet_identifier_bytes(),
        flags_and_length(root_layer_length(slot_count)),
        root_vector_bytes(),
        cid_bytes(cid),
    ])


# The framing layer counts from the place it begins,
# eighty-eight bytes and whatever slots it wins.
def framing_layer_length(slot_count):
    return 88 + slot_count


# The framing vector is two, and two it shall stay,
# the other values are for some other day.
def framing_vector_bytes():
    return struct.pack("!L", VECTOR_E131_DATA_PACKET)


# Sixty-four bytes is the room for a name,
# padded with nulls so each is the same.
def source_name_bytes(name):
    return name.encode("utf-8")[:63].ljust(64, b"\x00")


# Priority lives between zero and two hundred,
# we clamp it in case a caller has blundered.
def priority_byte(priority):
    return bytes([max(0, min(200, priority))])


# Synchronization is something we never do,
# so the address is zero, and the bytes are two.
def sync_address_bytes():
    return struct.pack("!H", 0)


# The sequence counts upward and wraps at the top,
# two fifty-five, then zero, it never will stop.
def sequence_byte(sequence):
    return bytes([sequence & 0xFF])


# No preview, no terminate, no forcing of sync,
# the options are zero, as blank as dry ink.
def options_byte():
    return bytes([0])


# The universe number is sixteen bits long,
# big-endian order, or everything's wrong.
def universe_bytes(universe):
    return struct.pack("!H", universe)


# Stack all of the framing fields into one slice,
# seventy-seven bytes, which is oddly precise.
def build_framing_layer(name, priority, sequence, universe, slot_count):
    return b"".join([
        flags_and_length(framing_layer_length(slot_count)),
        framing_vector_bytes(),
        source_name_bytes(name),
        priority_byte(priority),
        sync_address_bytes(),
        sequence_byte(sequence),
        options_byte(),
        universe_bytes(universe),
    ])


# The DMP layer comes last and is small,
# eleven plus slots is the length of it all.
def dmp_layer_length(slot_count):
    return 11 + slot_count


# Set Property is two, and it's all that we send,
# no other message, from start to the end.
def dmp_vector_byte():
    return bytes([VECTOR_DMP_SET_PROPERTY])


# Address and data type, an A and a one,
# nobody remembers why, but it's done.
def address_and_data_type_byte():
    return bytes([0xA1])


# The first property address is zero, of course,
# the START code lives there, right at the source.
def first_property_address_bytes():
    return struct.pack("!H", 0x0000)


# We step through the properties one at a time,
# an increment of two would be a crime.
def address_increment_bytes():
    return struct.pack("!H", 0x0001)


# The count is the slots and the START code as well,
# forget the plus one and it all goes to hell.
def property_value_count_bytes(slot_count):
    return struct.pack("!H", slot_count + 1)
