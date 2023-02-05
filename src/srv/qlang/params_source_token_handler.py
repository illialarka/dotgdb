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


class ParamsSourceTokenHandler(BaseTokenHandler):

    def can_handle(self, source):
        return source == 'params'

    def handle(self, agent, event):
        breakpoint_thread_id = event.thread_id
        stackframes = agent.vm.get_thread(breakpoint_thread_id).get_stackframes()

        logger.debug (f'Queries method parameters for the {breakpoint_thread_id}. Frames: {len(stackframes)}.') 

        if stackframes is None or len(stackframes) == 0:
            logger.info('There are not stackframes.')
            return

        method_params = []
        for stackframe in stackframes:
            parameters = stackframe.get_method().get_params()

            for method_param in parameters:
                param_value = stackframe.get_param_value(method_param)
                actual_value = None

                if isinstance(param_value, PrimitiveTypeValue):
                    actual_value = param_value.value 

                method_params.append(MethodLocalInfo(method_param.index, method_param.name, actual_value))

        return method_params 

