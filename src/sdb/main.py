import argparse
import logging
import utils
import dbg_session 
import dbg_agent
import exceptions
import logging
import commands.selector as selector
import traceback

logger = logging.getLogger()

def cli():
    argument_parser = argparse.ArgumentParser(
            prog = "SDB Client",
            description = "Mono Soft Debugger client")

    argument_parser.add_argument("executable")
    argument_parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose logging level")
    argument_parser.add_argument("-p", "--port", help= "port to connect in case of attaching")
    argument_parser.add_argument("-a", "--address", help="address to connect in case of attaching", default="127.0.0.1")

    arguments = argument_parser.parse_args()
    utils.configure_logger(arguments.verbose)

    session = dbg_session.DbgSession()
    agent = dbg_agent.DbgAgent()

    try:
        session.run(arguments)
        agent.start(True, session.port, 10)
        #agent.vm.resume()
    except exceptions.ExecutableNotFound:
        logger.info("Couldn't find an executable to run. Ensure it exists in {arguments.executable}.")

    while True:
        try:
            input_command = input("sdb> ").split(" ")

            command_alias = None
            command_arguments = None

            if len(input_command) == 0:
                print ("No command specified.")
                continue

            if len(input_command) >= 1:
                command_alias = input_command[0]
                command_arguments = input_command[1:]

            command = selector.select_command(command_alias)

            if command is None:
                print("Unknown command. Try 'help' or 'supported_commands' to see all supported commands")
                continue

            print(command.execute(agent, command_arguments))
        except exceptions.ExitException:
            logger.info("Exit requested. Closing session and kill processes.")
            session.exit()
            agent.stop()
            return
        except Exception:
            print (traceback.format_exc())

if __name__ == "__main__":
    cli()
