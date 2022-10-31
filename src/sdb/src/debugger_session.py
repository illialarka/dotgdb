import interop.debugger_args as debugger_args

class DebuggerSession():

    def __init__(self):
        self.breakpoints = dict()
        self.assemblies = dict()

    def target_output(is_std_err, data):
        pass

class DebuggerSessionBridge():

    def __init__(self, debugger_session: DebuggerSession):
        self.debugger_session = debugger_session

    def push_target_output(self, is_std_err, data):
        self.debugger_session.target_output(is_std_err, data)
