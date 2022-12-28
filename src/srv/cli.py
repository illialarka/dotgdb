from state_store_service import StateStoreService, EXECUTION_STATE_RUNNING, EXECUTION_STATE_RECORDING
from nbstreamreader import NonBlockingStreamReader
import argparse
import logging
import utils
import session
import agent
import exceptions
import logging
import constants
import event_handlers
import commands.selector as selector

logger = logging.getLogger()
state_store_service = StateStoreService()


def cli():
    argument_parser = argparse.ArgumentParser(
        prog="sdb",
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

    arguments = argument_parser.parse_args()
    utils.configure_logger(arguments)

    _session, _agent = session.Session(), agent.Agent()

    # set event handlers
    _agent.events_callbacks[constants.EVENT_KIND_BREAKPOINT] = event_query_wrapper 
    _agent.events_callbacks[constants.EVENT_KIND_VM_START] = event_handlers.on_vm_start
    _agent.events_callbacks[constants.EVENT_KIND_STEP] = event_handlers.on_step

    try:
        _session.run(
            arguments.executable, arguments.port), _agent.start(
            True, _session.port, 10)

        # those calls are required to create appdomain and load types
        _agent.vm.resume(), _agent.vm.suspend()
        state_store_service.state.executable_path = arguments.executable
    except exceptions.ExecutableNotFound:
        print(
            "Couldn't find an executable to run. Ensure it exists in {arguments.executable}.")
        return

    try:
        process_interaction(_agent, _session)
    finally:
        _session.exit(), _agent.stop()


def process_interaction(agent, session):
    non_blocking_stream_reader = NonBlockingStreamReader(
        session.debug_process.stdout)
    state_store_service = StateStoreService()

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

            input_command = input(
                f"sdb{state_postfix}> ").split(" ")

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

def event_query_wrapper(event):
    if state_store_service.state.execution_state == EXECUTION_STATE_RECORDING:
        event_descriptor = None 

        for desc in state_store_service.state.event_descriptors:
            if desc.request_id == event.request_id:
                event_descriptor = desc 

        if event_descriptor is None:
            print('Event descriptor was not found.')
            return
        
        print('event query found kinda executed:')
        print(event_descriptor.event_query.query)

if __name__ == "__main__":
    cli()
