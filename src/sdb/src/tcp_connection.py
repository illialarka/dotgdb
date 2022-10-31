import src.connection as connection
import socket

class TcpConnection(connection.Connection):

    def __init__(self, socket):
        super().__init__(socket)
        self.__socket.settimeout(50)

    def connect(self):
        buffer_length = len(self.__handshake_token)

        self.__buffer = bytearray(buffer_length)
        recieved_bytes = self.recieve(0, buffer_length)

        if recieved_bytes == 0 or recieved_bytes != buffer_length or self.__buffer.decode("utf-8") != self.__handshake_token:
            raise Exception("Handshake failed")

    # before reveiving data from the socket, we need to make
    # sure that the buffer is large enough to hold the data
    def recieve(self, offset, length):
        buffer_offset = 0

        while buffer_offset < length:
            recieved_bytes = self.__recieve()

            if received_bytes == 0:
                return buffer_offset

            buffer_offset += recieved_bytes

        return buffer_offset

    def __send(self):
        return self.__socket.send(self.__buffer)

    def __recieve(self):
        return self.__socket.recv_into(self.__buffer, len(self.__buffer))
