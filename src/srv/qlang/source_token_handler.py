from base_token_handler import BaseTokenHandler

class SourceTokenHandler(BaseTokenHandler):

    def can_handle(self, source):
        return source == 'threads'

    def handle(self):
        threads = self._agent.vm.get_all_threads()
        return threads if threads else []
