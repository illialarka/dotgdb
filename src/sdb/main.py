import argparse
import logging
import utils
import session
import exceptions
import logging
import agent
import commands.selector as selector

logger = logging.getLogger()

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
    dbg_agent = agent.DbgAgent()

    try:
        dbg_session.run(arguments)
        dbg_agent.start(True, dbg_session.port, 10)

        while True:
            input_command = input("sdb> ")

            command = selector.select_command(input_command)

            if command is None:
                print("Unknown command")
                continue

            print (command.execute(dbg_agent, []))

    except exceptions.ExitException:
        logger.info("Exit requested. Closing session and kill processes.")
        dbg_session.exit()
        dbg_agent.stop()
    except exceptions.ExecutableNotFound:
        logger.info("Couldn't find an executable to run. Ensure it exists in {arguments.executable}.")
    except Exception as unhandled_exception:
        logger.error(unhandled_exception)
        logger.info("Closing all session on exception.")
        dbg_session.exit()
        dbg_agent.stop()

if __name__ == "__main__":
    main()
