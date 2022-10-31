import src.interop.packet_header as interop

class TestPacketHeader:

    def test_packet_header_parses_as_expected(self):
        header = interop.PacketHeader(bytearray([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C]))
        assert header.id == 0x01020304
        assert header.flags == 0x05
        assert header.command_set == 0x06
        assert header.command == 0x07