import constants
from cli_context import CliContextService 

def on_vm_start(event):
    print('Event <(kind = {0}), (request_id = {1}), (thread_id = {2})>'
        .format(constants.EVENT_FRIENDLY_NAME[event.event_kind], event.request_id, event.thread_id))

def on_breakpoint(event):
    print('Event <(kind = {0}), (request_id = {1}), (thread_id = {2})>'
        .format(constants.EVENT_FRIENDLY_NAME[event.event_kind], event.request_id, event.thread_id))
    context_service = CliContextService() 
    context_service.break_on(event)

def on_step(event):
    print('Event <(kind = {0}), (request_id = {1}), (thread_id = {2})>'
        .format(constants.EVENT_FRIENDLY_NAME[event.event_kind], event.request_id, event.thread_id))
    print('Step over')
    cli_context_service = CliContextService() 
    cli_context_service.break_on(event)

