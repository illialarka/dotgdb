import src.interop.packet_header as packet_header
import socket

class Connection:

    def __init__(self, socket: socket.socket):
        # socket handshare token used to initiate handshake with debugger
        self.__handshake_token = "DWP-Handshake"
        self.__socket = socket
        self.__buffer = bytearray()

    def connect(self):
        self.__buffer = bytearray(len(self.__handshake_token))
        self.__transport_get__(len(buffer))
        cbuffer = buffer.decode("utf-8")

        if cbufer != self.__handshake_token:
            raise Exception("Handshake failed")

    def close(self):
        self.__socket.close()
        self.__buffer = bytearray()
