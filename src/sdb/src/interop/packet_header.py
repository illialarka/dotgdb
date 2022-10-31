import src.utils.byte_utils as byte_utils

"""
Represets packet header. For more information see:
https://www.mono-project.com/docs/advanced/runtime/docs/soft-debugger-wire-format
"""
class PacketHeader:
    # defined size of the packet header. See more wire format documentation
    length = 11

    def __init__(self, packet: bytearray):
        self.__packet = packet

        # parse header
        offset = 0
        self.id, offset = byte_utils.extract_int(packet, offset)
        self.flags, offset = byte_utils.extract_byte(packet, offset)
        self.command_set, offset = byte_utils.extract_byte(packet, offset)
        self.command, offset = byte_utils.extract_byte(packet, offset)

    def is_reply_packet(self):
        return self.flags & 0x80

    def packet_length(self):
        return byte_utils.extract_int(self.__packet, 0)
