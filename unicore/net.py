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


# Some other program may sit on the port,
# so we offer to share it, like a good sport.
def allow_address_reuse(sock):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, "SO_REUSEPORT"):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)


# Bind to all interfaces, whichever are there,
# on whatever port number the caller will share.
def bind_to_port(sock, port):
    sock.bind(("", port))


# Blocking would stall the whole video frame,
# so we never wait, and we feel no shame.
def make_non_blocking(sock):
    sock.setblocking(False)
