import threading
from collections import namedtuple

lock = threading.Lock()

BreakEventDescriptor = namedtuple(
    'BreakEventDescriptor',
    ['request_id', 'thread_id', 'friendly_event_kind_name'])

class CliContext:
    executable = None
    breakpoints = []
    # is set to break event descriptor in case
    # of interruption
    state = None

    # manages CLI state
    # When it is True CLI redirects all programm output to stdout
    # When it is False CLI can accept commands like 'info' 'break' etc.
    is_running = False

class CliContextService:
    def __init__(self):
        self._context = CliContext
    
    def set_executable(self, executable):
        lock.acquire()
        self._context.executable = executable
        lock.release()
   
    def get_executable(self):
        return self._context.executable

    def get_runinng(self):
        # I think we should not synchronize it
        return self._context.is_running

    def get_state_as_string(self):
        if self._context.state is None:
            return ''
        return f'(at breakpoint {self._context.state.request_id})'
    
    def start_running_executable(self):
        lock.acquire()
        self._context.is_running = True
        lock.release()

    def break_on(self, event):
        lock.acquire()
        request_id = event.request_id
        thread_id = event.thread_id

        break_descriptor = BreakEventDescriptor(
            request_id=request_id,
            thread_id=thread_id,
            # leav it as it is for now
            friendly_event_kind_name='Breakpoint')
        
        self._context.breakpoints.append(break_descriptor)
        self._context.is_running = False

        lock.release()
