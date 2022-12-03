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

class StepOverModifier:
    def __init__(self, thread_id):
        self.thread_id = thread_id

    def encode(self):
        return (
            sdbtypes.encode_integral(constants.MOD_KIND_STEP, 1) +
            sdbtypes.encode_integral(self.thread_id, 4) +
            sdbtypes.encode_integral(constants.STEP_SIZE_LINE, 8) +
            sdbtypes.encode_integral(constants.STEP_DEPTH_OVER, 16))
