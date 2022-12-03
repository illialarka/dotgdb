from commands.info_command import InfoCommand
from commands.resume_command import ResumeCommand
from commands.exit_command import ExitCommand
from commands.breakpoint_command import BreakpointCommand
from commands.thread_stackframe_command import ThreadStackframeCommand
from commands.print_command import PrintCommand
from commands.step_command import StepCommand

supported_commands = set([
    InfoCommand(),
    ResumeCommand(),
    ExitCommand(),
    BreakpointCommand(),
    ThreadStackframeCommand(),
    PrintCommand(),
    StepCommand()
])

def select_command(input_command):
    for command in supported_commands:
        if input_command in command.aliases:
            return command
    return None
