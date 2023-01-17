from qlang.base_token_handler import BaseTokenHandler
from state_store_service import StateStoreService
import logging

logger = logging.getLogger()
state_store_service = StateStoreService()


class ObjectsSourceTokenHandler(BaseTokenHandler):

    def can_handle(self, source):
        return source == 'objects'

    def handle(self, agent):
        breakpoint_thread_id = state_store_service.state.event_descritor.thread_id
        stackframes = agent.vm.get_thread(breakpoint_thread_id).get_stackframes()

        if stackframes is None or len(stackframes) == 0:
            logger.info('Can not get stackframe for some reason.')
            return

        locals = []
        for stackframe in stackframes:
            method_locals = stackframe.get_method().get_locals()

            for method_local in method_locals:
                locals.append(method_local)

        return [self._format_method_local(method_local)
            for method_local in locals]
    
    def _format_method_local(self, method_local):
        return dict(index=method_local.index, name=method_local.name)

