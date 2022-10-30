import ..utils.byte_utils as byte_utils

class PacketHeader:

    def __init__(self, packet: bytearray):
        self.__packet = packet

        # parse header
        offset = 0

