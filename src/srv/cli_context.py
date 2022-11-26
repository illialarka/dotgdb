class CliContext:
    executable = None
    state = ''
    breakpoints = []
    # manages CLI state
    # When it is True CLI redirects all programm output to stdout
    # When it is False CLI can accept commands like 'info' 'break' etc.
    is_running = False