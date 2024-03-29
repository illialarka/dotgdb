from commands.info_command import InfoCommand
from commands.resume_command import ResumeCommand
from commands.exit_command import ExitCommand
from commands.breakpoint_command import BreakpointCommand
from commands.thread_stackframe_command import ThreadStackframeCommand
from commands.print_command import PrintCommand
from commands.step_command import StepCommand
from commands.query_command import QueryCommand
from commands.record_command import RecordCommand
from commands.threads_command import ThreadsCommand
from commands.supported_commands import SupportedCommands

supported_commands = set([
    SupportedCommands(),
    InfoCommand(),
    ResumeCommand(),
    ExitCommand(),
    BreakpointCommand(),
    ThreadStackframeCommand(),
    PrintCommand(),
    StepCommand(),
    QueryCommand(),
    RecordCommand(),
    ThreadsCommand()
])


def select_command(input_command):
    for command in supported_commands:
        if input_command in command.aliases:
            return command
    return None
