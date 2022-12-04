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
        self._continue = True

        def _populate_queue(stream, queue):
            while True and self._continue:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    return EndOfStreamException

        self._thread = Thread(
            target=_populate_queue, args=(
                self._stream, self._queue))
        self._thread.deamon = True
        self._thread.start()

    def readline(self, timeout=None):
        try:
            return self._queue.get(block=timeout is not None, timeout=timeout)
        except BaseException:
            return None

    def close(self):
        self._continue = False


class EndOfStreamException(Exception):
    pass
