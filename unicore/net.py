# 川の水
# 網ですくえば
# 光る粒
import socket

SACN_PORT = 5568


# Two thirty-nine, two fifty-five, high byte, then low,
# that is where packets for a universe go.
def multicast_address_for(universe):
    return "239.255.%d.%d" % (universe >> 8, universe & 0xFF)


# A datagram socket, IPv4 and plain,
# nothing about it is hard to explain.
def open_udp_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
