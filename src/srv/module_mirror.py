import sdbtypes
import constants
import buffer_stream

from collections import namedtuple

ModuleInfo = namedtuple(
    "ModuleInfo",
    ["basename", "scopename", "fullname", "guid", "assembly_id"])

class ModuleMirror:

    def __init__(self, agent, id):
        self._agent = agent
        self._info = None

        self.id = id

    def __str__(self):
        return (
            "Module Mirror: basename = {0}, scopename = {1}, "
            "fullname = {2}, guid = {3}").format(
            self.get_basename(), self.get_scopename(),
            self.get_fullname(), self.get_guid())

    def get_basename(self):
        return self._get_info().basename

    def get_scopename(self):
        return self._get_info().scopename

    def get_fullname(self):
        return self._get_info().fullname

    def get_guid(self):
        return self._get_info().guid

    def get_assembly(self):
        return self._agent.vm.get_assembly(self._get_info().assembly_id)

    def _get_info(self):
        if self._info is None:
            answer = self._agent.send_command(
                constants.CMDSET_MODULE,
                constants.CMD_MODULE_GET_INFO,
                sdbtypes.encode_int(self.id))

            stream = buffer_stream.BufferStream(answer.data)
            basename = stream.get_string()
            scopename = stream.get_string()
            fullname = stream.get_string()
            guid = stream.get_string()
            assembly_id = stream.get_int()

            self._info = ModuleInfo(
                basename, scopename, fullname, guid, assembly_id)

        return self._info
