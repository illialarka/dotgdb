import os.path as path
import asyncio.subprocess
import logging
import utils
import subprocess
import exceptions
import traceback

logger = logging.getLogger()


class Session:
    '''
    Represents debugger session with access to a debug process.
    '''

    def __init__(self):
        self.debug_process = None
        self.port = None
        self.executable = None
        self.address = "127.0.0.1"

    def run(self, executable_path, port):
        if port is not None:
            raise Exception("Attaching to process is not implemented yet")

        if executable_path is not None:
            self.executable_path = executable_path
            if not path.exists(self.executable_path):
                raise exceptions.ExecutableNotFound()

            self._run_debug_server()

    def exit(self):
        if self.debug_process is None:
            return

        try:
            return_code = self.debug_process.kill()

            if return_code is not None:
                print(
                    "Debugger process exited with {0} code.".format(return_code))
        except BaseException:
            print(traceback.format_exception())

    def _run_debug_server(self):
        self.port = utils.find_port()
        logger.debug(
            f"Debug server is going to run on {self.address}:{self.port}")

        command = f"mono --debug --debugger-agent=transport=dt_socket,server=y,address={self.address}:{self.port} {self.executable_path}"

        logger.debug(f"command: {command}")

        self.debug_process = subprocess.Popen(
            [command],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True)

        self.debug_process.poll()
