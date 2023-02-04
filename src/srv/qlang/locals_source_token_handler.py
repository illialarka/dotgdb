from qlang.base_token_handler import BaseTokenHandler
from state_store_service import StateStoreService
from collections import namedtuple
from interop.sdbtypes import PrimitiveTypeValue
import logging

logger = logging.getLogger()
state_store_service = StateStoreService()


MethodLocalInfo = namedtuple(
    'MethodLocalInfo',
    ['id', 'name', 'value'])


class LocalsSourceTokenHandler(BaseTokenHandler):

    def can_handle(self, source):
        return source == 'locals'

    def handle(self, agent, event):
        breakpoint_thread_id = event.thread_id
        stackframes = agent.vm.get_thread(breakpoint_thread_id).get_stackframes()

        logger.debug (f'Queries stackframes for the {breakpoint_thread_id}. Frames: {len(stackframes)}.') 

        if stackframes is None or len(stackframes) == 0:
            logger.info('There are not stackframes.')
            return

        stackframe_locals = []
        for stackframe in stackframes:
            method_locals = stackframe.get_method().get_locals()

            for method_local in method_locals:
                local_value = stackframe.get_local_value(method_local)
                actual_value = None
                if isinstance(local_value, PrimitiveTypeValue):
                    actual_value = local_value.value 

                stackframe_locals.append(MethodLocalInfo(method_local.index, method_local.name, actual_value))

        return stackframe_locals    

