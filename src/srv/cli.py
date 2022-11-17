import argparse
import logging
import utils
import session 
import agent 
import exceptions
import logging
import constants
import commands.selector as selector

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

    _session, _agent = session.Session(), agent.Agent()

    _agent.events_callbacks[constants.EVENT_KIND_BREAKPOINT] = handle_breakpoint_event 

    try:
        _session.run(arguments), _agent.start(True, _session.port, 10)
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

                command.execute(_agent, command_arguments)

            # process domain exceptions
            except exceptions.ExitException:
                logger.info("Exit requested. Closing session and kill processes.")
                return
    finally:
        _session.exit(), _agent.stop()

def handle_breakpoint_event(event):
    print ("Event Happend:<kind {0}, data {1}, thread {2}>"
        .format(constants.EVENT_FRIENDLY_NAME[event.event_kind], event.request_id, event.thread_id))

if __name__ == "__main__":
    cli()