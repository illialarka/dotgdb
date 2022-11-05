# For more information see:
# https://www.mono-project.com/docs/advanced/runtime/docs/soft-debugger-wire-format/

import constants

from struct import unpack_from, pack
from collections import namedtuple

DecodeInfo = namedtuple("DecodeInfo", ["object", "used_length"])

def encode_integral(value, size):
    return value.to_bytes(size, byteorder="big", signed=(value < 0))

def decode_integral(buffer, size):
    value = int.from_bytes(buffer[:size], byteorder="big")
    return DecodeInfo(value, size)

def decode_byte(buffer):
    return decode_integral(buffer, 1)

def encode_byte(value):
    return encode_integral(value, 1)

def decode_short(buffer):
    return decode_integral(buffer, 2)

def encode_short(value):
    return encode_integral(value, 2)

def decode_int(buffer):
    return decode_integral(buffer, 4)

def encode_int(value):
    return encode_integral(value, 4)

def decode_long(buffer):
    return decode_integral(buffer, 8)

def encode_long(value):
    return encode_integral(value, 8)

def encode_float(value):
    return pack(">f", value)

def decode_float(buffer):
    return DecodeInfo(unpack_from(">f", buffer)[0], 4)

def encode_double(value):
    return pack(">d", value)

def decode_double(buffer):
    return DecodeInfo(unpack_from(">d", buffer)[0], 8)

def encode_string(value):
    length_prefix = encode_int(len(value))
    data = value.encode(encoding="ascii")
    return length_prefix + data

def decode_string(buffer):
    str_length, used_length = decode_int(buffer)
    value = buffer[4:4 + str_length].decode(encoding="ascii")
    return DecodeInfo(value, str_length + used_length)

def encode_array(values, elem_encoder, *encoder_args):
    length_prefix = encode_int(len(values))
    data = b"".join([elem_encoder(i, *encoder_args) for i in values])
    return length_prefix + data

def decode_array_known_size(buffer, elem_decoder, count):
    value = []
    data_offset = 0
    for i in range(count):
        decoded_element, used_length = elem_decoder(buffer[data_offset:])
        data_offset += used_length
        value.append(decoded_element)
    return DecodeInfo(value, data_offset)

def decode_array(buffer, elem_decoder):
    array_length = decode_int(buffer).object
    decode_info = decode_array_known_size(
        buffer[4:], elem_decoder, array_length)
    return DecodeInfo(decode_info.object, decode_info.used_length + 4)

class NullValue:
    def __str__(self):
        return "Null value"

    def encode(self):
        return encode_byte(constants.MONO_TYPE_NULL)

    @staticmethod
    def decode(buffer):
        return DecodeInfo(NullValue(), 0)

class VoidValue:
    def __str__(self):
        return "Void value"

    def encode(self):
        assert False, "Void value should never be sended to debugger"

    @staticmethod
    def decode(buffer):
        return DecodeInfo(VoidValue(), 0)

class PrimitiveTypeValue:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "'Primitive' type, value = {0}".format(self.value)

    def encode(self):
        return (encode_byte(self.type) + self._encode_value())

    def _encode_value(self):
        if self.type == constants.MONO_TYPE_BOOLEAN:
            return encode_int(int(self.value))

        elif (self.type == constants.MONO_TYPE_I1 or
              self.type == constants.MONO_TYPE_U1 or
              self.type == constants.MONO_TYPE_CHAR or
              self.type == constants.MONO_TYPE_I2 or
              self.type == constants.MONO_TYPE_U2 or
              self.type == constants.MONO_TYPE_I4 or
              self.type == constants.MONO_TYPE_U4):
            return encode_int(self.value)

        elif self.type == constants.MONO_TYPE_R4:
            return encode_float(self.value)

        elif self.type == constants.MONO_TYPE_R8:
            return encode_double(self.value)

        elif (self.type == constants.MONO_TYPE_I8 or
              self.type == constants.MONO_TYPE_U8):
            return encode_long(self.value)

        else:
            assert False, "Provided mono type is not 'primitive'"

    @staticmethod
    def decode(buffer, type):
        if type == constants.MONO_TYPE_BOOLEAN:
            value, used_length = decode_int(buffer)
            value = (value != 0)

        elif (type == constants.MONO_TYPE_I1 or
              type == constants.MONO_TYPE_U1 or
              type == constants.MONO_TYPE_CHAR or
              type == constants.MONO_TYPE_I2 or
              type == constants.MONO_TYPE_U2 or
              type == constants.MONO_TYPE_I4 or
              type == constants.MONO_TYPE_U4):
            value, used_length = decode_int(buffer)

        elif type == constants.MONO_TYPE_R4:
            value, used_length = decode_float(buffer)

        elif (type == constants.MONO_TYPE_I8 or
              type == constants.MONO_TYPE_U8):
            value, used_length = decode_long(buffer)

        elif type == constants.MONO_TYPE_R8:
            value, used_length = decode_double(buffer).object

        else:
            assert False, "Unknown mono primitive type: {0}".format(type)

        return DecodeInfo(PrimitiveTypeValue(type, value), used_length)

class PtrValue:
    def __init__(self, ptr):
        self.ptr = ptr

    def __str__(self):
        return "Ptr value: {0}".format(self.ptr)

    def encode(self):
        return encode_byte(constants.MONO_TYPE_PTR) + encode_long(self.ptr)

    @staticmethod
    def decode(buffer):
        ptr = decode_long(buffer)
        return DecodeInfo(PtrValue(ptr), 8)

class ObjectValue:
    def __init__(self, object_id):
        self.object_id = object_id

    def __str__(self):
        return "Object value, id = {0}".format(self.object_id)

    def encode(self):
        return (
            encode_byte(constants.MONO_TYPE_OBJECT) +
            encode_int(self.object_id))

    @staticmethod
    def decode(buffer):
        object_id = decode_int(buffer).object
        return DecodeInfo(ObjectValue(object_id), 4)

class ValueTypeValue:
    def __init__(self, is_enum, type_id, fields_values):
        self.is_enum = is_enum
        self.type_id = type_id
        self.fields_values = fields_values

    def __str__(self):
        return (
            "Value type, enum = {0}, type id = {1}, values = {2}".format(
                self.is_enum,
                self.type_id,
                [str(v) for v in self.fields_values]))

    def encode(self):
        encoded_fields = encode_array(self.fields_values, encode_variant_value)
        return (
            encode_byte(constants.MONO_TYPE_VALUETYPE) +
            encode_byte(0) +
            encoded_fields)

    @staticmethod
    def decode(buffer):
        is_enum = decode_byte(buffer).object == 1
        type_id = decode_int(buffer[1:]).object
        values, values_length = (
            decode_array(buffer[5:], decode_variant_value))
        return DecodeInfo(
            ValueTypeValue(is_enum, type_id, values),
            5 + values_length)

def decode_variant_value(buffer):
    type = decode_byte(buffer).object

    if type == constants.MONO_TYPE_NULL:
        value, value_length = NullValue.decode(buffer[1:])

    elif type == constants.MONO_TYPE_VOID:
        value, value_length = VoidValue.decode(buffer[1:])

    elif (type == constants.MONO_TYPE_BOOLEAN or
          type == constants.MONO_TYPE_I1 or
          type == constants.MONO_TYPE_U1 or
          type == constants.MONO_TYPE_CHAR or
          type == constants.MONO_TYPE_I2 or
          type == constants.MONO_TYPE_U2 or
          type == constants.MONO_TYPE_I4 or
          type == constants.MONO_TYPE_U4 or
          type == constants.MONO_TYPE_R4 or
          type == constants.MONO_TYPE_I8 or
          type == constants.MONO_TYPE_U8 or
          type == constants.MONO_TYPE_R8 or
          type == constants.MONO_TYPE_PTR):
        value, value_length = PrimitiveTypeValue.decode(buffer[1:], type)

    elif (type == constants.MONO_TYPE_STRING or
          type == constants.MONO_TYPE_SZARRAY or
          type == constants.MONO_TYPE_OBJECT or
          type == constants.MONO_TYPE_CLASS or
          type == constants.MONO_TYPE_ARRAY):
        value, value_length = ObjectValue.decode(buffer[1:])

    elif type == constants.MONO_TYPE_VALUETYPE:
        value, value_length = ValueTypeValue.decode(buffer[1:])

    else:
        assert False, "Unknown mono type: {0}".format(type)

    return DecodeInfo(value, 1 + value_length)

def encode_variant_value(value):
    return value.encode()
