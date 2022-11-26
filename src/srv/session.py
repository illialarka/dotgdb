import os.path as path
import logging
import utils
import subprocess
import exceptions
import traceback

logger = logging.getLogger()

class Session:

    def __init__(self):
        self.breakpoints = [] 
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
            return_code = self.debug_process.kill()

            if return_code is not None:
                print ("Debugger process exited with {0} code.".format(return_code))
        except:
            print (traceback.format_exception()) 
    
    def set_breakpoint(self):
        pass
     
    def unset_breakpoint(self):
        pass

    def _run_debug_server(self, executable):
        self.port = utils.find_port()
        logger.debug(f"Debug server is going to run on {self.address}:{self.port}")

        command = f"mono --debug --debugger-agent=transport=dt_socket,server=y,address={self.address}:{self.port} {executable}"

        logger.debug(f"command: {command}")

        self.debug_process = subprocess.Popen(
                [ command ],
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=True)

        return_code = self.debug_process.poll()