import argparse
import logging
import utils
import debug_session 
import debug_agent 
import exceptions
import logging
import commands.selector as selector

# Hi here! If someone ever get to this commit (by accident or whatever)
# please, know, I do not have so much knowledge of python and may not know
# something, something very useful and helpful, but I will figure out and 
# start this open source project.

# TODO
# 1. Start with simple commands 
# 1.1 Get type with codelocations
# 1.2 Set breakpoint on type codeloc
# 1.3 Catch entering bt
# 1.4 Show locals on catching
# 1.5 continue debugging

logger = logging.getLogger()

def cli():
    argument_parser = argparse.ArgumentParser(
            prog = "SDB Client",
            description = "Mono Soft Debugger client")

    argument_parser.add_argument("executable")
    argument_parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose logging level")
    argument_parser.add_argument("-p", "--port", help= "port to connect in case of attaching")
    argument_parser.add_argument("-a", "--address", help="address to connect in case of attaching", default="127.0.0.1")
    argument_parser.add_argument("--logFile", help="specifies log files. If not provided, logger will not write to file", default=None)
    argument_parser.add_argument( "--plain", help="configures provide output in plain text", type=bool, default=True) 
    argument_parser.add_argument( "--json", help="configures provide output in json", type=bool, default=False) 

    arguments = argument_parser.parse_args()
    utils.configure_logger(arguments)

    session, agent = debug_session.DbgSession(), debug_agent.DbgAgent()

    try:
        session.run(arguments), agent.start(True, session.port, 10)
        agent.vm.resume()
    except exceptions.ExecutableNotFound:
        print("Couldn't find an executable to run. Ensure it exists in {arguments.executable}.")

    try:
        while True:
            try:
                input_command = input("sdb> ").split(" ")

                command_alias = None
                command_arguments = None

                if len(input_command) == 0:
                    print ("No command specified.")
                    continue

                if len(input_command) >= 1:
                    command_alias = input_command[0].strip()
                    command_arguments = input_command[1:]

                command = selector.select_command(command_alias)

                if command is None:
                    print("Unknown command. Try 'help' or 'supported_commands' to see all supported commands")
                    continue

                command.execute(agent, command_arguments)

            # process domain exceptions
            except exceptions.ExitException:
                logger.info("Exit requested. Closing session and kill processes.")
                return
    finally:
        session.exit(), agent.stop()

if __name__ == "__main__":
    cli()