from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Event
from queue import Queue, Empty
from collections import namedtuple
from interop import buffer_stream, constants, vm_snapshot, sdbtypes

import events_data as ev
import exceptions
import logging
import time

logger = logging.getLogger()

EventRequest = namedtuple("EventRequest", ["event_kind", "request_id"])
Packet = namedtuple("Packet", ["header", "data"])


class Agent:

    def __init__(self):
        self._socket = None
        self._server_socket = None
        self._is_listening = False
        self._packet_counter = 65536
        self._replies_events = {}
        self._events_queue = Queue()
        self._vm_started_event = Event()
        self._listening_started_event = Event()

        self.vm = None
        self.events_callbacks = {}

    def start(self, initiate, port, timeout=None):
        if not initiate:
            logger.debug("Starting at {0}.".format(port))
            self._socket = socket(AF_INET, SOCK_STREAM)
            self._socket.bind(("127.0.0.1", port))
            self._socket.listen(1)

            self._socket.settimeout(timeout)
            self._server_socket, self._server_endpoint = self._socket.accept()
        else:
            logger.debug("Connecting to {0}.".format(port))
            self._server_endpoint = ("127.0.0.1", port)
            self._server_socket = socket(AF_INET, SOCK_STREAM)

            max_attempts, success = 10, False
            while not success and max_attempts > 0:
                logger.info(
                    "Attempting to connect ({0} attempts left).".format(max_attempts))

                response_code = self._server_socket.connect_ex(
                    self._server_endpoint)
                if response_code == 0:
                    success = True
                else:
                    self._server_socket = socket(AF_INET, SOCK_STREAM)
                    max_attempts -= 1
                    time.sleep(1)

        logger.debug(
            "Receiving handhsake from {0}.".format(self._server_endpoint))
        self._server_socket.settimeout(timeout)
        handshake = self._server_socket.recv(len(constants.RIGHT_HANDSHAKE))
        self._server_socket.settimeout(None)
        if handshake != constants.RIGHT_HANDSHAKE:
            raise ConnectionError(
                "Bad handshake received ({0}).".format(handshake))

        self._server_socket.sendall(handshake)

        logger.debug("Running threads.")

        self._listening_thread = Thread(target=self._listen)
        self._listening_thread.name = "sdb listening thread"
        self._listening_thread.daemon = True
        self._listening_thread.start()

        self._listening_started_event.wait()

        self._events_thread = Thread(target=self._process_events)
        self._events_thread.name = "sdb events thread"
        self._events_thread.daemon = True
        self._events_thread.start()

        logger.debug("Waiting for virtual machine start event.")
        self._vm_started_event.wait()

        logger.debug("Debugger agent is fully started.")

    def stop(self, kill_vm=None):
        if not self._is_listening:
            return

        if kill_vm is not None:
            if kill_vm:
                self.vm.exit()
            else:
                self.vm.suspend()
                self.vm.dispose()

        self._is_listening = False

        try:
            if self._socket is not None:
                self._socket.close()
            if self._server_socket is not None:
                self._server_socket.close()
        except BaseException:
            logger.info("Agent is stopped.")

    def send_command(self, command_set, command_id, params=b""):
        packet = (
            sdbtypes.encode_int(constants.PACKET_HEADER_SIZE + len(params)) +
            sdbtypes.encode_int(self._packet_counter) +
            sdbtypes.encode_byte(constants.PACKET_FLAG_CMD) +
            sdbtypes.encode_byte(command_set) +
            sdbtypes.encode_byte(command_id) +
            params)

        event = Event()
        self._replies_events[self._packet_counter] = event
        self._packet_counter += 1
        self._server_socket.sendall(packet)
        event.wait()

        error_code = buffer_stream.BufferStream(
            event.answer.header).skip(9).get_short()
        error = exceptions.error_code_to_exception(error_code)
        if error is not None:
            raise error

        return event.answer

    def enable_event(self, event_kind, suspend_policy, *modifiers):
        modifiers_data = b"".join([m.encode() for m in modifiers])
        params = (
            sdbtypes.encode_byte(event_kind) +
            sdbtypes.encode_byte(suspend_policy) +
            sdbtypes.encode_byte(len(modifiers)) +
            modifiers_data)

        answer = self.send_command(
            constants.CMDSET_EVENT_REQUEST,
            constants.CMD_EVENT_REQUEST_SET,
            params)

        error_code = buffer_stream.BufferStream(
            answer.header).skip(9).get_short()
        error = exceptions.error_code_to_exception(error_code)
        if error is not None:
            raise error

        request_id = buffer_stream.BufferStream(answer.data).get_int()
        event_request = EventRequest(event_kind, request_id)

        return event_request

    def disable_event(self, event_request):
        params = (
            sdbtypes.encode_byte(event_request.event_kind) +
            sdbtypes.encode_int(event_request.request_id))

        self.send_command(
            constants.CMDSET_EVENT_REQUEST,
            constants.CMD_EVENT_REQUEST_CLEAR,
            params)

    def disable_all_breakpoints(self):
        self.send_command(
            constants.CMDSET_EVENT_REQUEST,
            constants.CMD_EVENT_REQUEST_CLEAR_ALL_BREAKPOINTS)

    def _process_events(self):
        logger.info("Processing events started")
        while self._is_listening:
            # Non-zero timeout to stop when listening will be stopped
            try:
                suspend_policy, events_data = self._events_queue.get(timeout=1)
            except Empty:
                continue

            self._on_event_set(suspend_policy, events_data)
            self._events_queue.task_done()

        logger.debug("event processing stopped")

    def _listen(self):
        logger.debug("listening started")

        self._is_listening = True
        self._listening_started_event.set()

        while self._is_listening:
            try:
                header = self._server_socket.recv(constants.PACKET_HEADER_SIZE)
            except Exception as ex:
                self.stop()
                break
            if len(header) == 0:
                self.stop()
                break

            packet_length = buffer_stream.BufferStream(header).get_int()
            data_length = packet_length - constants.PACKET_HEADER_SIZE

            if data_length > 0:
                try:
                    data = self._server_socket.recv(data_length)
                except BaseException:
                    self.stop()
                    break
                if len(data) == 0:
                    self.stop()
                    break
            else:
                data = b""

            try:
                self._process_packet(header + data)
            except BaseException:
                logger.debug(
                    "exception during packet processing:",
                    exc_info=True)

        logger.debug("listening stopped")

    def _process_packet(self, packet):
        packet_flag = buffer_stream.BufferStream(packet).skip(8).get_byte()
        if packet_flag == constants.PACKET_FLAG_REPLY:
            self._process_reply_packet(packet)
        else:
            self._process_cmd_packet(packet)

    def _process_cmd_packet(self, packet):
        packet_stream = buffer_stream.BufferStream(packet).skip(9)

        cmdset = packet_stream.get_byte()
        cmd = packet_stream.get_byte()
        assert (cmdset == constants.CMDSET_EVENT and
                cmd == constants.CMD_EVENT_COMPOSITE)

        suspend_policy = packet_stream.get_byte()
        events_count = packet_stream.get_int()

        events_data = []
        for i in range(events_count):
            event_data = ev.create_event_data(packet_stream)
            events_data.append(event_data)

        self._events_queue.put((suspend_policy, events_data))

    def _process_reply_packet(self, packet):
        id = buffer_stream.BufferStream(packet).skip(4).get_int()
        if id in self._replies_events:
            event = self._replies_events.pop(id)
            event.answer = Packet(
                packet[:constants.PACKET_HEADER_SIZE],
                packet[constants.PACKET_HEADER_SIZE:])
            event.set()

    def _on_event_set(self, suspend_policy, events_data):
        for event_data in events_data:
            if event_data.event_kind == constants.EVENT_KIND_VM_START:
                self.vm = vm_snapshot.VmMirror(
                    self, event_data.root_appdomain_id)
                self._vm_started_event.set()

            if event_data.event_kind in self.events_callbacks:
                self.events_callbacks[event_data.event_kind](event_data, self)

    def _self_connect(self):
        max_attempts, success = 10, False
        while not success and max_attempts > 0:
            logger.info("Attempting to connect {0}".format(max_attempts))

            rc = self._server_socket.connect_ex(self._server_endpoint)
            if rc == 0:
                success = True
            else:
                self._server_socket = socket(AF_INET, SOCK_STREAM)
                max_attempts -= 1
                time.sleep(1)
