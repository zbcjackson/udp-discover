import nanoid
import socket
import threading
from time import sleep

PORT = 37520


def _init_upd():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return udp


def _create_daemon(target):
    return threading.Thread(target=target, daemon=True)


class Node:
    def __init__(self):
        self._id = nanoid.generate(size=10)
        self._send_udp = _init_upd()
        self._receive_udp = _init_upd()
        self._broadcasting_thread = _create_daemon(self._broadcasting)
        self._receiving_thread = _create_daemon(self._receiving)
        self._nodes = {}

    def start(self):
        self._receive_udp.bind(("", PORT))
        self._send_udp.settimeout(0.2)
        self._broadcasting_thread.start()
        self._receiving_thread.start()

    @property
    def nodes(self):
        return self._nodes

    def _broadcasting(self):
        while True:
            self._send_udp.sendto(self._id.encode('utf-8'), ('<broadcast>', PORT))
            sleep(0.5)

    def _receiving(self):
        while True:
            data, addr = self._receive_udp.recvfrom(1024)
            self._nodes[data.decode('utf-8')] = str(addr)
