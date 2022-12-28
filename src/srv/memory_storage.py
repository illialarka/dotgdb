class InMemoryStorage:
    
    def __init__(self, size):
        self._data = {}
        self._size = size
