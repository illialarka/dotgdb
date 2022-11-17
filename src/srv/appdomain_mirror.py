import sdbtypes
import constants
import buffer_stream

class AppDomainMirror:

    def __init__(self, agent, id):
        self._agent = agent
        self._name = None
        self._entry_assembly_id = None
        self._corlib_assembly_id = None

        self.id = id

    def __str__(self):
        return "AppDomain <(id = {0}), (name = {1})>".format(self.id, self.get_name())

    def get_name(self):
        if self._name is None:
            answer = self._agent.send_command(
                constants.CMDSET_APPDOMAIN,
                constants.CMD_APPDOMAIN_GET_NAME,
                sdbtypes.encode_int(self.id))

            self._name = buffer_stream.BufferStream(answer.data).get_string()

        return self._name

    def get_assemblies(self):
        answer = self._agent.send_command(
            constants.CMDSET_APPDOMAIN,
            constants.CMD_APPDOMAIN_GET_ASSEMBLIES,
            sdbtypes.encode_int(self.id))

        ids = buffer_stream.BufferStream(answer.data).get_array(sdbtypes.decode_int)
        return [self._agent.vm.get_assembly(id) for id in ids]

    def get_entry_assembly(self):
        if self._entry_assembly_id is None:
            answer = self._agent.send_command(
                constants.CMDSET_APPDOMAIN,
                constants.CMD_APPDOMAIN_GET_ENTRY_ASSEMBLY,
                sdbtypes.encode_int(self.id))

            self._entry_assembly_id = buffer_stream.BufferStream(answer.data).get_int()

        return self._agent.vm.get_assembly(self._entry_assembly_id)

    def get_corlib_assembly(self):
        if self._corlib_assembly_id is None:
            answer = self._agent.send_command(
                constants.CMDSET_APPDOMAIN,
                constants.CMD_APPDOMAIN_GET_CORLIB_ASSEMBLY,
                sdbtypes.encode_int(self.id))

            self._corlib_assembly_id = buffer_stream.BufferStream(answer.data).get_int()

        return self._agent.vm.get_assembly(self._corlib_assembly_id)

    def get_assembly_by_name(self, name):
        for assembly in self.get_assemblies():
            if assembly.get_name() == name:
                return assembly
        return None