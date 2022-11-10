import os.path as path
import logging
import utils
import subprocess
import exceptions
import time

logger = logging.getLogger()

class DbgSession:

    def __init__(self):
        self.debug_process = None
        self.port = None
        self.executable = None
        self.address = "127.0.0.1"

    def __del__(self):
        self.exit()

    def run(self, arguments):
        if arguments.port is not None:
            raise Exception("Attaching to process is not implemented yet")

        # here we should run debugger agent and
        if arguments.executable is not None:
            self.executable = arguments.executable
            if not path.exists(self.executable):
                raise exceptions.ExecutableNotFound()

            self._run_debug_server(self.executable)

    def exit(self):
        if self.debug_process is None:
            return

        try:
            self.debug_process.kill()
        except Exception as ex:
            print (ex) 


    def _run_debug_server(self, executable):
        self.port = utils.find_port()
        logger.debug(f"debug server is going to run on {self.address}:{self.port}")

        command = f"mono --debug --debugger-agent=transport=dt_socket,server=y,address={self.address}:{self.port} {executable}"

        logger.debug(f"command: {command}")

        # well, it should wait until we connect to server
        # for now leave as is
        # in future will add checking to make sure it is still alive
        self.debug_process = subprocess.Popen(
                [ command ],
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True)

        return_code = self.debug_process.poll()
