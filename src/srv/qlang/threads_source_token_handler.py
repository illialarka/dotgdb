from qlang.base_token_handler import BaseTokenHandler


class ThreadsSourceTokenHandler(BaseTokenHandler):

    def can_handle(self, source):
        return source == 'threads'

    def handle(self, agent):
        threads = agent.vm.get_all_threads()
        return threads if threads else []
