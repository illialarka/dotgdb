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

    event_descriptors = []
    state = State()

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
        self._event_descriptors.append(event_descriptor)

    def clear_events(self):
        self._event_descriptors = []

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

        self._state.execution_state = EXECUTION_STATE_AT_BREAKPOINT 
        self._state.event_descritor = event_descriptor 

        lock.release()


EXECUTION_STATE_RUNNING = 1
EXECUTION_STATE_AT_BREAKPOINT = 2
EXECUTION_STATE_CONFIGURING = 3

class State:

    def __init__(self):
        self.executable_path = None 
        self.event_descritor = None
        self.execution_state = EXECUTION_STATE_CONFIGURING 
