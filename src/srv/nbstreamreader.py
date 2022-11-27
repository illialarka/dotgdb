from threading import Thread
from queue import Queue

class NonBlockingStreamReader:
    '''
    Represents non-blocking stream reader.
    Runs separate thread and implements asynchronous communication
    using queue.
    '''
    def __init__(self, stream):
        self._stream = stream 
        self._queue = Queue()

        def _populate_queue(stream, queue):
            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    return 

        self._thread = Thread(target = _populate_queue, args=(self._stream, self._queue))
        self._thread.deamon = True
        self._thread.start()

    def readline(self, timeout = None):
        try:
            return self._queue.get(block = timeout is not None, timeout = timeout)
        except:
            return None 
