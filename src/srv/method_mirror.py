import sdbtypes
import constants
import buffer_stream
from collections import namedtuple

MethodDebugInfo = namedtuple(
    "MethodDebugInfo",
    ["code_size", "source_filename", "code_locations"])

CodeLocation = namedtuple("CodeLocation", ["il_offset", "line_number"])

MethodParamInfo = namedtuple(
    "MethodParamInfo",
    ["call_convention", "params_count",
     "generic_params_count", "return_type_id", "params"])

MethodLocalsInfo = namedtuple(
    "MethodLocalsInfo",
    ["locals_count", "locals"])

class MethodParam:

    def __init__(self, agent, type_id, name, index):
        self._agent = agent
        self._type_id = type_id

        self.index = index
        self.name = name

    def __str__(self):
        return "Method param, name = {0}".format(self.name)

    def get_type(self):
        return self._agent.vm.get_type(self._type_id)

class MethodLocal:

    def __init__(self, agent, type_id, name, scope, index):
        self._agent = agent
        self._type_id = type_id

        self.index = index
        self.name = name
        self.scope = scope

    def __str__(self):
        return "Method local, name = {0}".format(self.name)

    def get_type(self):
        return self._agent.vm.get_type(self._type_id)

class MethodMirror:

    def __init__(self, agent, id):
        self._agent = agent
        self._name = None
        self._type_id = None
        self._debug_info = None
        self._param_info = None
        self._locals_info = None
        self._body = None

        self.id = id
    
    def __dict__(self):
        return {
            'Id': self.id,
            'Name': self.get_name(),
            'Size': self.get_code_size(),
            'File': self.get_source_filename()
        }

    def __str__(self):
        return "Method <(id = {0}), (name = {1}), (size = {2})> at {3}".format(
            self.id, self.get_name(), self.get_code_size(), self.get_source_filename())

    def get_name(self):
        if self._name is None:
            answer = self._agent.send_command(
                constants.CMDSET_METHOD,
                constants.CMD_METHOD_GET_NAME,
                sdbtypes.encode_int(self.id))

            self._name = buffer_stream.BufferStream(answer.data).get_string()

        return self._name

    def get_type(self):
        if self._type_id is None:
            answer = self._agent.send_command(
                constants.CMDSET_METHOD,
                constants.CMD_METHOD_GET_DECLARING_TYPE,
                sdbtypes.encode_int(self.id))

            self._type_id = buffer_stream.BufferStream(answer.data).get_int()

        return self._agent.vm.get_type(self._type_id)

    def get_code_size(self):
        return self._get_debug_info().code_size

    def get_source_filename(self):
        return self._get_debug_info().source_filename

    def get_code_locations(self):
        return self._get_debug_info().code_locations

    def get_il_offset_by_line_number(self, line_number):
        offsets = []
        for loc in self.get_code_locations():
            if loc.line_number == line_number:
                offsets.append(loc.il_offset)

        return min(offsets)

    def get_line_number_by_il_offset(self, il_offset):
        for loc in reversed(self.get_code_locations()):
            if loc.il_offset <= il_offset:
                return loc.line_number

    def get_body(self):
        if self._body is None:
            answer = self._agent.send_command(
                constants.CMDSET_METHOD,
                constants.CMD_METHOD_GET_BODY,
                sdbtypes.encode_int(self.id))

            self._body = answer.data

        return self._body

    def get_call_convention(self):
        return self._get_param_info().call_convention

    def get_params_count(self):
        return self._get_param_info().params_count

    def get_generic_params_count(self):
        return self._get_param_info().generic_params_count

    def get_return_type(self):
        return self._agent.vm.get_type(self._get_param_info().return_type_id)

    def get_params(self):
        return self._get_param_info().params

    def get_locals_count(self):
        return self._get_locals_info().locals_count

    def get_locals(self):
        return self._get_locals_info().locals

    def _get_debug_info(self):
        if self._debug_info is None:
            def decode_code_location(buffer):
                il_offset = sdbtypes.decode_int(buffer).object
                line_number = sdbtypes.decode_int(buffer[4:]).object
                return sdbtypes.DecodeInfo(
                    CodeLocation(il_offset, line_number), 8)

            answer = self._agent.send_command(
                constants.CMDSET_METHOD,
                constants.CMD_METHOD_GET_DEBUG_INFO,
                sdbtypes.encode_int(self.id))

            stream = buffer_stream.BufferStream(answer.data)
            code_size = stream.get_int()
            source_filename = stream.get_string()
            lines_map = stream.get_array(decode_code_location)

            self._debug_info = MethodDebugInfo(
                code_size, source_filename, lines_map)

        return self._debug_info

    def _get_param_info(self):
        if self._param_info is None:
            answer = self._agent.send_command(
                constants.CMDSET_METHOD,
                constants.CMD_METHOD_GET_PARAM_INFO,
                sdbtypes.encode_int(self.id))

            stream = buffer_stream.BufferStream(answer.data)
            call_convention = stream.get_int()
            params_count = stream.get_int()
            generic_params_count = stream.get_int()
            return_type_id = stream.get_int()
            params_type_ids = [stream.get_int() for i in range(params_count)]
            params_names = [stream.get_string() for i in range(params_count)]

            assert len(params_type_ids) == params_count
            assert len(params_names) == params_count

            params = [
                MethodParam(self._agent, type_id, name, index)
                for type_id, name, index
                in zip(params_type_ids, params_names, range(params_count))]

            self._param_info = MethodParamInfo(
                call_convention,
                params_count,
                generic_params_count,
                return_type_id,
                params)

        return self._param_info

    def _get_locals_info(self):
        if self._locals_info is None:
            answer = self._agent.send_command(
                constants.CMDSET_METHOD,
                constants.CMD_METHOD_GET_LOCALS_INFO,
                sdbtypes.encode_int(self.id))

            stream = buffer_stream.BufferStream(answer.data)
            locals_count = stream.get_int()
            types_ids = [stream.get_int() for i in range(locals_count)]
            names = [stream.get_string() for i in range(locals_count)]
            scopes = [
                (stream.get_int(), stream.get_int())
                for i
                in range(locals_count)]

            assert len(types_ids) == locals_count
            assert len(names) == locals_count
            assert len(scopes) == locals_count

            locals = [
                MethodLocal(self._agent, type_id, name, scope, index)
                for type_id, name, scope, index
                in zip(types_ids, names, scopes, range(locals_count))]

            self._locals_info = MethodLocalsInfo(locals_count, locals)

        return self._locals_info
