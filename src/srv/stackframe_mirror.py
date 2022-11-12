import constants
import types
import buffer_stream

class StackFrameMirror:
    def __init__(
            self, agent, id, parent_thread_id,
            method_id, il_offset, flags):
        self._agent = agent
        self._parent_thread_id = parent_thread_id
        self._method_id = method_id
        self._flags = flags
        self._this = None

        self.il_offset = il_offset
        self.id = id

    def __str__(self):
        return "Stackframe at {0}:{1} (this = {2})".format(
            self.get_method().get_name(),
            self.get_source_line(),
            self.get_this())

    def get_method(self):
        return self._agent.vm.get_method(self._method_id)

    def get_source_line(self):
        return self.get_method().get_line_number_by_il_offset(self.il_offset)

    def get_this(self):
        if self._this is None:
            params = (
                types.encode_int(self._parent_thread_id) +
                types.encode_int(self.id))
            answer = self._agent.send_command(
                constants.CMDSET_STACK,
                constants.CMD_STACK_GET_THIS,
                params)

            stream = buffer_stream.BufferStream(answer.data)

            self._this = stream.get_variant_value()

        return self._this

    def get_param_value(self, method_param):
        return self.get_params_values([method_param])[0]

    def get_params_values(self, method_params):
        positions = [- p.index - 1 for p in method_params]
        return self._get_values(positions)

    def get_local_value(self, method_local):
        return self.get_locals_values([method_local])[0]

    def get_locals_values(self, method_locals):
        positions = [p.index for p in method_locals]
        return self._get_values(positions)

    def set_param_value(self, method_param, value):
        self.set_params_values([method_param], [value])

    def set_params_values(self, method_params, values):
        positions = [- p.index - 1 for p in method_params]
        self._set_values([(p, v) for p, v in zip(positions, values)])

    def set_local_value(self, method_local, value):
        self.set_locals_values([method_local], [value])

    def set_locals_values(self, method_locals, values):
        positions = [p.index for p in method_locals]
        self._set_values([(p, v) for p, v in zip(positions, values)])

    def _get_values(self, positions):
        params = (
            types.encode_int(self._parent_thread_id) +
            types.encode_int(self.id) +
            types.encode_array(positions, types.encode_int))
        answer = self._agent.send_command(
            constants.CMDSET_STACK,
            constants.CMD_STACK_GET_VALUES,
            params)

        stream = buffer_stream.BufferStream(answer.data)
        values = stream.get_array_known_size(
            types.decode_variant_value, len(positions))

        return values

    def _set_values(self, positions_values):
        def encode_position_value(position_value):
            return (
                types.encode_int(position_value[0]) +
                types.encode_variant_value(position_value[1]))

        params = (
            types.encode_int(self._parent_thread_id) +
            types.encode_int(self.id) +
            types.encode_array(positions_values, encode_position_value))
        self._agent.send_command(
            constants.CMDSET_STACK,
            constants.CMD_STACK_SET_VALUES,
            params)
