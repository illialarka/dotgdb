import constants
from cli_context import CliContextService

cli_context_service = CliContextService()


def on_vm_start(event):
    write_event_basic_info(event)


def on_breakpoint(event):
    write_event_basic_info(event)
    cli_context_service.break_on(event)


def on_step(event):
    write_event_basic_info(event)
    cli_context_service.break_on(event)


def write_event_basic_info(event):
    print('Event {0} received with request identifier {1} at the thread {2}.' .format(
        constants.EVENT_FRIENDLY_NAME[event.event_kind], event.request_id, event.thread_id))
