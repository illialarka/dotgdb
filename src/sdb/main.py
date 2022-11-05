import argparse
import logging 
import utils
import session
import exceptions
import logging

logger = logging.getLogger()

# entry point for application which will read from stdin and write to stdout
# parsing commands and sending them to debugger in proer format
# 1. consume commands from stdin
# 1.1. parse commands
# 1.2 if command is run, start debugger process
# 2. send command to debugger
# 3. read response from debugger
# 4. send response to stdout
# 5. repeat 1-4
def main():
    argument_parser = argparse.ArgumentParser(
            prog = "SDB",
            description = "Mono Soft Debugger agent")

    argument_parser.add_argument("executable")
    argument_parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose logging level")
    argument_parser.add_argument("-p", "--port", help= "port to connect in case of attaching")
    argument_parser.add_argument("-a", "--address", help="address to connect in case of attaching", default="127.0.0.1")

    arguments = argument_parser.parse_args()
    utils.configure_logger(arguments.verbose)

    debugger_session = session.DebuggerSession()

    try:
        debugger_session.run_session(arguments)
    except exceptions.ExecutableNotFound:
        logger.info("Couldn't find an executable to run. Ensure it exists in {arguments.executable}.") 
    except Exception as unhandled_exception:
        logger.error(unhandled_exception)
        logger.info("Closing all session on exception.")
        debugger_session.exit() 


if __name__ == "__main__":
    main()

