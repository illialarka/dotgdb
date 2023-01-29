from state_store_service import StateStoreService, EXECUTION_STATE_RECORDING
from interop import constants

state_store_service = StateStoreService()


def on_vm_start(event, agent):
    write_event_basic_info(event)


def on_breakpoint(event, agent):
    if state_store_service.state.execution_state == EXECUTION_STATE_RECORDING:
        enabled_breakpoints = state_store_service.state.event_descriptors

        for event_breakpoint in enabled_breakpoints:
            if event_breakpoint.event_query is not None:
                try:
                    print('query data')
                    queries_dataset = event_breakpoint.event_query.execute(
                        agent, event)
                    print(queries_dataset.__str__())
                except Exception as e:
                    print(e)
                finally:
                    agent.vm.resume()
                    continue
        return
    write_event_basic_info(event)
    state_store_service.triger_event(event)


def on_step(event, agent):
    write_event_basic_info(event)
    state_store_service.triger_event(event)


def write_event_basic_info(event):
    print('Event {0} received with request identifier {1} at the thread {2}.' .format(
        constants.EVENT_FRIENDLY_NAME[event.event_kind], event.request_id, event.thread_id))
