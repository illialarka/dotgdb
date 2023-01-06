import sdbtypes
import constants
import buffer_stream


class ObjectMirror:

    def __init__(self, agent, id):
        self._agent = agent
        self._type_id = None
        self._appdomain_id = None
        self._address = None
        self._string_value = None
        self._array_dimensions = None

        self.id = id

    def __str__(self):
        return "id = {0}, type = {1}, address = {2}".format(self.id, self.get_type(), self.get_address())

    def get_type(self):
        if self._type_id is None:
            answer = self._agent.send_command(
                constants.CMDSET_OBJECT,
                constants.CMD_OBJ_GET_TYPE,
                sdbtypes.encode_int(self.id))

            self._type_id = buffer_stream.BufferStream(answer.data).get_int()

        return self._agent.vm.get_type(self._type_id)

    def get_appdomain(self):
        if self._appdomain_id is None:
            answer = self._agent.send_command(
                constants.CMDSET_OBJECT,
                constants.CMD_OBJ_GET_DOMAIN,
                sdbtypes.encode_int(self.id))

            self._appdomain_id = buffer_stream.BufferStream(
                answer.data).get_int()

        return self._agent.vm.get_appdomain(self._appdomain_id)

    def get_is_collected(self):
        answer = self._agent.send_command(
            constants.CMDSET_OBJECT,
            constants.CMD_OBJ_IS_COLLECTED,
            sdbtypes.encode_int(self.id))

        is_collected = (buffer_stream.BufferStream(answer.data).get_int() == 1)
        return is_collected

    def get_address(self):
        if self._address is None:
            answer = self._agent.send_command(
                constants.CMDSET_OBJECT,
                constants.CMD_OBJ_GET_ADDRESS,
                sdbtypes.encode_int(self.id))

            self._address = buffer_stream.BufferStream(answer.data).get_long()

        return self._address

    def get_string_value(self):
        if self._string_value is None:
            answer = self._agent.send_command(
                constants.CMDSET_STRING,
                constants.CMD_STR_GET_VALUE,
                sdbtypes.encode_int(self.id))

            self._string_value = buffer_stream.BufferStream(
                answer.data).get_string()

        return self._string_value

    def get_array_dimensions(self):
        if self._array_dimensions is None:
            def decode_dimension_info(buffer):
                length = sdbtypes.decode_int(buffer).object
                lower_bound = sdbtypes.decode_int(buffer[4:]).object
                return sdbtypes.DecodeInfo((length, lower_bound), 8)

            answer = self._agent.send_command(
                constants.CMDSET_ARRAY,
                constants.CMD_ARRAY_GET_LENGTH,
                sdbtypes.encode_int(self.id))

            stream = buffer_stream.BufferStream(answer.data)
            dimensions = stream.get_array(decode_dimension_info)

            self._array_dimensions = dimensions

        return self._array_dimensions

    def get_array_values(self, start_index, length):
        params = (
            sdbtypes.encode_int(self.id) +
            sdbtypes.encode_int(start_index) +
            sdbtypes.encode_int(length))
        answer = self._agent.send_command(
            constants.CMDSET_ARRAY,
            constants.CMD_ARRAY_GET_VALUES,
            params)

        values = buffer_stream.BufferStream(answer.data).get_array_known_size(
            sdbtypes.decode_variant_value, length)

        return values

    def set_array_values(self, start_index, array_values):
        params = (
            sdbtypes.encode_int(self.id) +
            sdbtypes.encode_int(start_index) +
            sdbtypes.encode_array(array_values, sdbtypes.encode_variant_value))
        self._agent.send_command(
            constants.CMDSET_ARRAY,
            constants.CMD_ARRAY_SET_VALUES,
            params)

    def get_field_value(self, field):
        return self.get_fields_values([field])[0]

    def get_fields_values(self, fields):
        ids = [f.id for f in fields]
        ids_encoded = sdbtypes.encode_array(ids, sdbtypes.encode_int)
        answer = self._agent.send_command(
            constants.CMDSET_OBJECT,
            constants.CMD_OBJ_GET_VALUES,
            sdbtypes.encode_int(self.id) + ids_encoded)

        values = buffer_stream.BufferStream(answer.data).get_array_known_size(
            sdbtypes.decode_variant_value, len(fields))
        return values

    def set_field_value(self, field, value):
        self.set_fields_values([(field, value)])

    def set_fields_values(self, fields_values):
        def encode_field_value(value):
            return (
                sdbtypes.encode_int(value[0].id) +
                sdbtypes.encode_variant_value(value[1]))

        self._agent.send_command(
            constants.CMDSET_OBJECT,
            constants.CMD_OBJ_SET_VALUES,
            sdbtypes.encode_int(self.id) +
            sdbtypes.encode_array(fields_values, encode_field_value))
