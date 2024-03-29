import threading
from interop.constants import EVENT_FRIENDLY_NAME, EVENT_KIND_BREAKPOINT
import logging
import csv


logger = logging.getLogger()
lock = threading.Lock()


class EventDescriptor:

    def __init__(
            self,
            request_id,
            thread_id,
            friendly_event_kind_name,
            source,
            line_number,
            method_name,
            event_query):
        self.request_id = request_id
        self.thread_id = thread_id
        self.friendly_event_kind_name = friendly_event_kind_name
        self.source = source
        self.line_number = line_number
        self.method_name = method_name
        self.event_query = event_query
        self.output_file = open(f'breakpoint_{request_id}_{method_name}_{line_number}.csv', 'w+', newline ='')
        self.csv_writer = csv.writer(self.output_file)


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
            line_number=line_number,
            event_query=None)
        self.state.event_descriptors.append(event_descriptor)

    def clear_events(self):
        self.state.event_descriptors = []

    def triger_event(self, event_request):
        lock.acquire()
        logger.info(event_request)
        request_id = event_request.request_id
        thread_id = event_request.thread_id

        event_descriptor = EventDescriptor(
            request_id=request_id,
            thread_id=thread_id,
            source=None,
            line_number=0,
            method_name=None,
            friendly_event_kind_name=EVENT_FRIENDLY_NAME[event_request.event_kind],
            event_query=None)

        self.state.execution_state = EXECUTION_STATE_AT_BREAKPOINT
        self.state.event_descritor = event_descriptor

        lock.release()


EXECUTION_STATE_RUNNING = 1
EXECUTION_STATE_AT_BREAKPOINT = 2
EXECUTION_STATE_CONFIGURING = 3
EXECUTION_STATE_RECORDING = 4

file = open('output_1.csv', 'w+', newline ='')


class State:
    executable_path = None
    event_descritor = None
    execution_state = EXECUTION_STATE_CONFIGURING
    event_descriptors = []
