import interop.constants as constants

# Will be populated with data according to event type


class EventData:
    pass


def create_event_data(stream):
    event_data = EventData()

    event_data.event_kind = stream.get_byte()
    event_data.request_id = stream.get_int()
    event_data.thread_id = stream.get_int()

    if event_data.event_kind == constants.EVENT_KIND_VM_START:
        _populate_vm_start_event_data(stream, event_data)
    elif (event_data.event_kind == constants.EVENT_KIND_APPDOMAIN_CREATE or
          event_data.event_kind == constants.EVENT_KIND_APPDOMAIN_UNLOAD):
        _populate_appdomain_event_data(stream, event_data)
    elif (event_data.event_kind == constants.EVENT_KIND_METHOD_ENTRY or
          event_data.event_kind == constants.EVENT_KIND_METHOD_EXIT):
        _populate_method_event_data(stream, event_data)
    elif (event_data.event_kind == constants.EVENT_KIND_ASSEMBLY_LOAD or
          event_data.event_kind == constants.EVENT_KIND_ASSEMBLY_UNLOAD):
        _populate_assembly_event_data(stream, event_data)
    elif event_data.event_kind == constants.EVENT_KIND_TYPE_LOAD:
        _populate_type_event_data(stream, event_data)
    elif event_data.event_kind == constants.EVENT_KIND_BREAKPOINT:
        _populate_breakpoint_event_data(stream, event_data)
    elif event_data.event_kind == constants.EVENT_KIND_STEP:
        _populate_step_event_data(stream, event_data)
    elif event_data.event_kind == constants.EVENT_KIND_EXCEPTION:
        _populate_exception_event_data(stream, event_data)

    return event_data


def _populate_vm_start_event_data(stream, event_data):
    event_data.root_appdomain_id = stream.get_int()


def _populate_appdomain_event_data(stream, event_data):
    event_data.appdomain_id = stream.get_int()


def _populate_method_event_data(stream, event_data):
    event_data.method_id = stream.get_int()


def _populate_assembly_event_data(stream, event_data):
    event_data.assembly_id = stream.get_int()


def _populate_type_event_data(stream, event_data):
    event_data.type_id = stream.get_int()


def _populate_breakpoint_event_data(stream, event_data):
    event_data.method_id = stream.get_int()
    event_data.il_offset = stream.get_long()


def _populate_step_event_data(stream, event_data):
    event_data.method_id = stream.get_int()
    event_data.il_offset = stream.get_long()


def _populate_exception_event_data(stream, event_data):
    event_data.exception_id = stream.get_int()
