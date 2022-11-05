import argparse
import logging
import utils
import session
import exceptions
import logging
import agent
import commands.selector as selector

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
            prog = "SDB Client",
            description = "Mono Soft Debugger client")

    argument_parser.add_argument("executable")
    argument_parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose logging level")
    argument_parser.add_argument("-p", "--port", help= "port to connect in case of attaching")
    argument_parser.add_argument("-a", "--address", help="address to connect in case of attaching", default="127.0.0.1")

    arguments = argument_parser.parse_args()
    utils.configure_logger(arguments.verbose)

    dbg_session = session.DbgSession()

    try:
        dbg_session.run(arguments)
        dbg_agent = agent.Agent()
        dbg_agent.start(True, dbg_session.port)

        while True:
            input_command = input("sdb> ")

            command = selector.select_command(input_command)

            if command is None:
                print("Unknown command")
                continue

            print (command.execute(dbg_agent.vm, []))

        # implement interactive mode
        # infinite loop with reading commands from stdin
        # and processing them using agent
    except exceptions.ExecutableNotFound:
        logger.info("Couldn't find an executable to run. Ensure it exists in {arguments.executable}.")
    except Exception as unhandled_exception:
        logger.error(unhandled_exception)
        logger.info("Closing all session on exception.")
        dbg_session.exit()

if __name__ == "__main__":
    main()
