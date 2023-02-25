from refreshers.refresher import Refresher
from state_store_service import StateStoreService
from collections import namedtuple

Breakpoint = namedtuple(
    "Breakpoint",
    ["id", "kind", "method", "source", "line_number", "query"])


class BreakpointsRefresher(Refresher):
    """
    Represents breakpoints state refresher.
    """

    def __init__(self):
        self.scope = "breakpoints"

    def execute(self, agent, socket):
        """
        Emits current breakpoint list to socket.  
        """
        state_store_service = StateStoreService()
        event_descriptors = state_store_service.state.event_descriptors

        breakpoints = []

        for event_descriptor in event_descriptors:
            breakpoints.append(
                Breakpoint(
                    id=event_descriptor.request_id,
                    kind=event_descriptor.friendly_event_kind_name,
                    method=event_descriptor.method_name,
                    source=event_descriptor.source,
                    query=event_descriptor.event_query,
                    line_number=event_descriptor.line_number)
                ._asdict())

        socket.emit(self.scope, {"content": breakpoints})
