import threading
from constants import EVENT_FRIENDLY_NAME, EVENT_KIND_BREAKPOINT
from collections import namedtuple

lock = threading.Lock()

EventDescriptor = namedtuple(
    'EventDescriptor',
    [
        'request_id',
        'thread_id',
        'friendly_event_kind_name',
        'source',
        'line_number',
        'method_name'])


class StateStoreService:

    def __init__(self):
        self.state = State

    def add_event(
            self,
            event_request,
            file_name,
            line_number,
            method_name):
        event_descriptor = EventDescriptor(
            request_id=event_request.request_id,
            # event_request does not have thread_id yet
            thread_id=0,
            friendly_event_kind_name=EVENT_FRIENDLY_NAME[EVENT_KIND_BREAKPOINT],
            source=file_name,
            method_name=method_name,
            line_number=line_number)
        self.state.event_descriptors.append(event_descriptor)

    def clear_events(self):
        self.state.event_descriptors = []

    def triger_event(self, event_request):
        lock.acquire()
        request_id = event_request.request_id
        thread_id = event_request.thread_id

        event_descriptor = EventDescriptor(
            request_id=request_id,
            thread_id=thread_id,
            source=None,
            line_number=0,
            method_name=None,
            friendly_event_kind_name=EVENT_FRIENDLY_NAME[event_request.event_kind])

        self.state.execution_state = EXECUTION_STATE_AT_BREAKPOINT
        self.state.event_descritor = event_descriptor

        lock.release()


EXECUTION_STATE_RUNNING = 1
EXECUTION_STATE_AT_BREAKPOINT = 2
EXECUTION_STATE_CONFIGURING = 3


class State:
    executable_path = None
    event_descritor = None
    execution_state = EXECUTION_STATE_CONFIGURING
    event_descriptors = []
