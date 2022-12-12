import exceptions

class BaseSourceHandler:

    def __init__(self, agent):
        self._agent = agent

    def can_handle(self, source):
        pass
        
    def retrieve(self):
        pass