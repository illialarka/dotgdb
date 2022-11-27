import threading
from collections import namedtuple

lock = threading.Lock()

BreakEventDescriptor = namedtuple(
    'BreakEventDescriptor',
    ['request_id', 'thread_id', 'friendly_event_kind_name'])


class CliContextService:
    def __init__(self):
        self._context = _cli_context 
    
    def add_breakpoint(self, event_request):
        break_event_descriptor = BreakEventDescriptor(
            request_id=event_request.request_id,
            # event_request does not have thread_id yet
            thread_id=0,
            # leave it as it is for now
            friendly_event_kind_name='Breakpoint')
        self._context.breakpoints.append(break_event_descriptor)

    def clear_breakpoints(self):
        self._context.breakpoints = []
    
    def set_executable(self, executable):
        lock.acquire()
        self._context.executable = executable
        lock.release()
   
    def get_executable(self):
        return self._context.executable

    def get_runinng(self):
        return self._context.is_running

    def get_breakpoints(self):
        return self._context.breakpoints

    def get_state_as_string(self):
        if self._context.state is None:
            return ''
        return f'(at breakpoint {self._context.state.request_id})'
    
    def start_running_executable(self):
        self._context.is_running = True

    def break_on(self, event):
        lock.acquire()
        request_id = event.request_id
        thread_id = event.thread_id

        break_descriptor = BreakEventDescriptor(
            request_id=request_id,
            thread_id=thread_id,
            # leave it as it is for now
            friendly_event_kind_name='Breakpoint')
        
        self._context.breakpoints.append(break_descriptor)
        self._context.is_running = False
        self._context.state = break_descriptor

        lock.release()

class _cli_context:
    executable = None
    breakpoints = []
    state = None
    is_running = False
