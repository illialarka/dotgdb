import src.utils.byte_utils as byte_utils

class TestByteUtils:
    def test_exctract_byte_returns_expected_offset(self):
        _, offset = byte_utils.extract_byte(bytearray([0x01, 0x02, 0x03]), 0)
        assert 1 == offset

    def test_exctract_byte_returns_expected_byte(self):
        byte, _ = byte_utils.extract_byte(bytearray([0x01, 0x02, 0x03]), 0)
        assert 0x01 == byte

    def test_exctract_int_returns_expected_offset(self):
        _, offset = byte_utils.extract_int(bytearray([0x01, 0x02, 0x03, 0x04]), 0)
        assert 4 == offset

    def test_exctract_int_returns_expected_number(self):
        number, _ = byte_utils.extract_int(bytearray([0x01, 0x02, 0x03, 0x04]), 0)
        assert number == 0x01020304

    def test_exctract_short_returns_expected_offset(self):
        _, offset = byte_utils.extract_short(bytearray([0x01, 0x02, 0x03, 0x04]), 0)
        assert 2 == offset

    def test_exctract_short_returns_expected_short(self):
        short, _ = byte_utils.extract_short(bytearray([0x01, 0x02, 0x03, 0x04]), 0)
        assert short == 0x0102
