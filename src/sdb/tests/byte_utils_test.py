import unittest
from sdb.utils import byte_utils

class TestsByteUtils(unittest.TestCase):

    def test_decode_byte_returns_expected_offset(self):
        _, offset = byte_utils.decode_byte(bytearray([1]), 0)
        self.assertEqual(1, offset)

    def test_decode_byte_returns_expected_byte(self):
        byte, _ = byte_utils.decode_byte(bytearray([2]), 0)
        self.assertEqual(2, byte)

    def test_decode_int_returns_expected_offset(self):
        _, offset = byte_utils.decode_int(bytearray([1, 2, 3, 4]), 0)
        self.assertEqual(4, offset)

    def test_decode_int_returns_expected_byte(self):
        byte, _ = byte_utils.decode_int(bytearray([1, 2, 3, 4]), 0)
        self.assertEqual(16909060, byte)

if __name__ == '__main__':
    unittest.main()
