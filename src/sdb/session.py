import os.path as path
import logging
import utils
import subprocess
import exceptions
import agent
import time

logger = logging.getLogger()

class DebuggerSession:
    debug_process = None
    debug_agent = None
    port = None
    executable = None
    address = "127.0.0.1"

    def run_session(self, arguments):
        if arguments.port is not None:
            pass

        # here we should run debugger agent and
        if arguments.executable is not None:

            if not path.exists(arguments.executable):
                raise exceptions.ExecutableNotFound()

            self._run_debug_server(arguments.executable)
            self._run_debug_agent()

    def exit(self):
        if DebuggerSession.debug_process is None:
            return

        DebuggerSession.debug_process.kill()
        DebuggerSession.debug_agent.stop()
        DebuggerSession.debug_process = None
        DebuggerSession.debug_agent = None

    def _run_debug_server(self, executable):
        DebuggerSession.port = utils.find_port()
        logger.debug(f"debug server is going to run on {DebuggerSession.address}:{DebuggerSession.port}")

        command = f"mono --debug --debugger-agent=transport=dt_socket,server=y,address={DebuggerSession.address}:{DebuggerSession.port} {executable}"

        logger.debug(f"command: {command}")

        # well, it should wait until we connect to server
        # for now leave as is
        # in future will add checking to make sure it is still alive
        DebuggerSession.debug_process = subprocess.Popen(
                [ command ],
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True)

        time.sleep(5)

        return_code = DebuggerSession.debug_process.poll()

    def _run_debug_agent(self):
        DebuggerSession.debug_agent = agent.Agent()
        DebuggerSession.debug_agent.start(True, DebuggerSession.port, 50)

        ag = DebuggerSession.debug_agent
        print (ag.vm.get_root_appdomain())
