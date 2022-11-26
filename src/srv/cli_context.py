import threading

lock = threading.Lock()

class CliContext:
    executable = None
    state = ''
    breakpoints = []

    # manages CLI state
    # When it is True CLI redirects all programm output to stdout
    # When it is False CLI can accept commands like 'info' 'break' etc.
    is_running = False

    def get_runinng():
        running = None
        lock.acquire()
        running = CliContext.is_running 
        lock.release()
        return running 

    def break_on():
        lock.acquire()
        CliContext.state = f'(at breakpoint)'
        CliContext.is_running = False
        lock.release()
