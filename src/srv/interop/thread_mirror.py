import sdbtypes
import constants
import buffer_stream
import stackframe_mirror as sm


class ThreadMirror:

    def __init__(self, agent, id):
        self._agent = agent
        self._name = None
        self._is_from_threadpool = None

        self.id = id

    def __str__(self):
        return "Thread {0}".format(self.id, self.get_name())

    def get_name(self):
        if self._name is None:
            answer = self._agent.send_command(
                constants.CMDSET_THREAD,
                constants.CMD_THREAD_GET_NAME,
                sdbtypes.encode_int(self.id))

            real_name = buffer_stream.BufferStream(answer.data).get_string()
            if real_name == "":
                self._name = "<unnamed thread (id = {0})>".format(self.id)
            else:
                self._name = real_name

        return self._name

    def get_is_from_threadpool(self):
        if self._is_from_threadpool is None:
            answer = self._agent.send_command(
                constants.CMDSET_THREAD,
                constants.CMD_THREAD_GET_INFO,
                sdbtypes.encode_int(self.id))

            self._is_from_threadpool = (
                buffer_stream.BufferStream(answer.data).get_byte() == 1)

        return self._is_from_threadpool

    def get_state(self):
        answer = self._agent.send_command(
            constants.CMDSET_THREAD,
            constants.CMD_THREAD_GET_STATE,
            sdbtypes.encode_int(self.id))

        state = buffer_stream.BufferStream(answer.data).get_int()
        return state

    def get_stackframes(self):
        def decode_frame(buffer):
            id = sdbtypes.decode_int(buffer).object
            method_id = sdbtypes.decode_int(buffer[4:]).object
            il_offset = sdbtypes.decode_int(buffer[8:]).object
            flags = sdbtypes.decode_byte(buffer[12:]).object

            mirror = sm.StackFrameMirror(
                self._agent, id, self.id, method_id, il_offset, flags)

            return sdbtypes.DecodeInfo(mirror, 13)

        params = (
            sdbtypes.encode_int(self.id) +
            sdbtypes.encode_int(0) +
            sdbtypes.encode_int(-1))

        answer = self._agent.send_command(
            constants.CMDSET_THREAD,
            constants.CMD_THREAD_GET_FRAME_INFO,
            params)

        stream = buffer_stream.BufferStream(answer.data)
        frames = stream.get_array(decode_frame)

        return frames
