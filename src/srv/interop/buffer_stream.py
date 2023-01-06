import sdbtypes


class BufferStream:
    def __init__(self, buffer):
        self.buffer = buffer
        self.offset = 0

    def skip(self, count):
        self.offset += count
        return self

    def reset(self):
        self.offset = 0
        return self

    def get_bytes(self, count):
        data = self.buffer[self.offset:self.offset + count]
        self.offset += count
        return data

    def get_byte(self):
        data = sdbtypes.decode_byte(self.buffer[self.offset:]).object
        self.offset += 1
        return data

    def get_short(self):
        data = sdbtypes.decode_short(self.buffer[self.offset:]).object
        self.offset += 2
        return data

    def get_int(self):
        data = sdbtypes.decode_int(self.buffer[self.offset:]).object
        self.offset += 4
        return data

    def get_long(self):
        data = sdbtypes.decode_long(self.buffer[self.offset:]).object
        self.offset += 8
        return data

    def get_float(self):
        data = sdbtypes.decode_float(self.buffer[self.offset:]).object
        self.offset += 4
        return data

    def get_double(self):
        data = sdbtypes.decode_double(self.buffer[self.offset:]).object
        self.offset += 8
        return data

    def get_string(self):
        data, used_length = sdbtypes.decode_string(self.buffer[self.offset:])
        self.offset += used_length
        return data

    def get_array(self, elem_decoder):
        data, used_length = (
            sdbtypes.decode_array(self.buffer[self.offset:], elem_decoder))
        self.offset += used_length
        return data

    def get_array_known_size(self, elem_decoder, count):
        data, used_length = (
            sdbtypes.decode_array_known_size(
                self.buffer[self.offset:], elem_decoder, count))
        self.offset += used_length
        return data

    def get_variant_value(self):
        data, used_length = sdbtypes.decode_variant_value(
            self.buffer[self.offset:])
        self.offset += used_length
        return data
