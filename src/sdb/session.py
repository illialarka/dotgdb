import logging
import utils
import subprocess

logger = logging.getLogger()

class DebuggerSession:

    def __init__(self):
        self.port = None
        self._debug_process = None
        
    # Based on aguments perform certain actions
    def run_session(self, arguments):
        if arguments.port is not None:
            # here we should implement attaching to debugger
            pass

        # here we should run debugger agent and  
        if arguments.executable is not None:
            logger.debug("run mono debugger for executable")
            self._run_debugger_agent(arguments.executable)

    def _run_debugger_agent(self, executable):
        self.port = utils.find_port()
        logger.debug(f"debug server is going to run on {self.port}")

        command = f'mono --debug --debugger-agent=transport=dt_socket,server=y,address=127.0.0.1:{self.port} /Users/illialarka/projects/DebuggableProgram/bin/Debug/net6.0/DebuggableProgram.dll'

        logger.debug(command)

        self._debug_process = subprocess.Popen(
                [ command ],
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True)

        while True:
            output = self._debug_process.stdout.readline()
            if output == '' and slef._debug_process.poll() is not None:
                break
            if output:
                print (output.strip())
        result_code = self._debug_process.poll()

