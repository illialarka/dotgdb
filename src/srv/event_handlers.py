import constants
from cli_context import CliContext

def on_vm_start(event):
    print('Event <(kind = {0}), (request_id = {1}), (thread_id = {2})>'
    .format(constants.EVENT_FRIENDLY_NAME[event.event_kind], event.request_id, event.thread_id))

def on_breakpoint(event):
    CliContext.state = f'(at bt {event.request_id})'
