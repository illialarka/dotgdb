from qlang.base_token_handler import BaseTokenHandler
import logging

logger = logging.getLogger()


class ThreadsSourceTokenHandler(BaseTokenHandler):

    def can_handle(self, source):
        return source == 'threads'

    def handle(self, agent):
        thread_mirrors = agent.vm.get_all_threads()

        if thread_mirrors is None or len(thread_mirrors) == 0:
            logger.info('There are not threads found.')
            return None
        
        return [self._format_thread_mirror(thread_mirror)
            for thread_mirror in thread_mirrors]
    
    def _format_thread_mirror(self, thread_mirror):
        return dict(id=thread_mirror.id, name= thread_mirror.get_name())
