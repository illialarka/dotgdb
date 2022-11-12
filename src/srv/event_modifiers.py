import sdbtypes
import constants

class LocationModifier:

    def __init__(self, method_id, il_offset):
        self.method_id = method_id
        self.il_offset = il_offset

    def encode(self):
        return (
            sdbtypes.encode_integral(constants.MOD_KIND_LOCATION_ONLY, 1) +
            sdbtypes.encode_integral(self.method_id, 4) +
            sdbtypes.encode_integral(self.il_offset, 8))
