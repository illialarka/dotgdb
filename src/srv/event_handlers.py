import constants
from state_store_service import StateStoreService

state_store_service = StateStoreService()


def on_vm_start(event):
    write_event_basic_info(event)


def on_breakpoint(event):
    write_event_basic_info(event)
    state_store_service.triger_event(event)


def on_step(event):
    write_event_basic_info(event)
    state_store_service.triger_event(event)


def write_event_basic_info(event):
    print('Event {0} received with request identifier {1} at the thread {2}.' .format(
        constants.EVENT_FRIENDLY_NAME[event.event_kind], event.request_id, event.thread_id))
