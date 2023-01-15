from qlang.base_token_handler import BaseTokenHandler


class ThreadsSourceTokenHandler(BaseTokenHandler):

    def can_handle(self, source):
        return source == 'threads'

    def handle(self, agent):
        print("hi from threads token source")
        threads = agent.vm.get_all_threads()

        if threads is None or len(threads) == 0:
            print('Agent returns no threads.')
            return None
        
        return threads