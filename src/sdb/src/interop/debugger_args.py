# represents basic arguments to run debugger
class DebuggerRunArgs:

    def __init__(slef, connection_provider, app_name, addres, debug_port, output_port,
        executable_name, runtime_prefix = None, env_vars = {}):
        self.max_connection_attempts = 1
        self.connection_attempt_timeout = 50 # seconds
        self.connection_provider = connection_provider
        self.app_name = app_name
        self.debug_port = debug_port
        self.output_port = output_port
        self.runtime_prefix = runtime_prefix
        self.env_vars = env_vars
        self.executable_name = executable_name

        if address is None:
            raise Exception("Address cannot be null")
        self.address = address

        if debug_port is None:
            raise Exception("Debug port cannot be null")
        self.debug_port = debug_port
