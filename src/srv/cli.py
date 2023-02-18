from state_store_service import StateStoreService, EXECUTION_STATE_RUNNING, EXECUTION_STATE_RECORDING
from interop.nbstreamreader import NonBlockingStreamReader
from interop.agent import Agent
from interop.constants import *
from commands import selector
from session import Session
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory 
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from server import process_server

import argparse
import logging
import utils
import exceptions
import logging
import event_handlers

logger = logging.getLogger()
state_store_service = StateStoreService()


def cli():
    argument_parser = argparse.ArgumentParser(
        prog="dotgdb",
        description="Mono Soft Debugger CLI")

    argument_parser.add_argument("executable")
    argument_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging level.")
    argument_parser.add_argument(
        "--logFile",
        help="Log file. If not provided, logger will not write to file.",
        default=None)
    argument_parser.add_argument(
        "-p", "--port", help="Port for debugger agent listen to.")
    argument_parser.add_argument(
        "-s",
        "--server",
        help="Indicating whether run it as server",
        action=argparse.BooleanOptionalAction)

    arguments = argument_parser.parse_args()
    utils.configure_logger(arguments)

    _session, _agent = Session(), Agent()

    try:
        if arguments.server:
            process_server(agent=_agent, session=_session, arguments=arguments)
        else: 
            process_interaction(agent=_agent, session=_session, arguments=arguments)
    finally:
        _session.exit(), _agent.stop()


def process_interaction(agent, session, arguments):
    agent.events_callbacks[EVENT_KIND_BREAKPOINT] = event_handlers.on_breakpoint
    agent.events_callbacks[EVENT_KIND_VM_START] = event_handlers.on_vm_start
    agent.events_callbacks[EVENT_KIND_STEP] = event_handlers.on_step

    try:
        session.run(
            arguments.executable, arguments.port), agent.start(
            True, session.port, 10)

        agent.vm.resume(), agent.vm.suspend()
        state_store_service.state.executable_path = arguments.executable
    except exceptions.ExecutableNotFound:
        logger.error(
            f"Couldn't find an executable to run. Ensure it exists in {arguments.executable}.")
        return

    non_blocking_stream_reader = NonBlockingStreamReader(
        session.debug_process.stdout)

    cli_history = FileHistory('.dotgdb-history') 
    cli_session = PromptSession(history=cli_history)

    while True:
        try:
            if state_store_service.state.execution_state == EXECUTION_STATE_RUNNING or state_store_service.state.execution_state == EXECUTION_STATE_RECORDING:
                output_line = non_blocking_stream_reader.readline(0.1)
                if output_line:
                    print(output_line.decode('utf-8'), end='')
                continue

            state_postfix = ''

            if state_store_service.state.event_descritor is not None:
                state_postfix = f'(at {state_store_service.state.event_descritor.request_id})'

            input_command = cli_session.prompt(
                f"dotgdb{state_postfix}> ", auto_suggest=AutoSuggestFromHistory()).split(" ")

            command_alias = None
            command_arguments = None

            if len(input_command) == 0:
                print("No command specified.")
                continue

            if len(input_command) >= 1:
                command_alias = input_command[0].strip()
                command_arguments = input_command[1:]

            command = selector.select_command(command_alias)

            if command is None:
                print(
                    "Unknown command. Try 'help' or 'supportedcommands' to see all supported commands.")
                continue

            command_result = command.execute(agent, command_arguments)

            if command_result is not None:
                print(command_result)

        # process domain exceptions
        except exceptions.ExitException:
            logger.info("Exit requested. Closing session and kill processes.")
            non_blocking_stream_reader.close()
            return

if __name__ == "__main__":
    cli()
