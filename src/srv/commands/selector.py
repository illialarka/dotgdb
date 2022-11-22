from commands.info_command import InfoCommand
from commands.resume_command import ResumeCommand
from commands.exit_command import ExitCommand
from commands.breakpoint_command import BreakpointCommand

supported_commands = set([
    InfoCommand(),
    ResumeCommand(),
    ExitCommand(),
    BreakpointCommand()
])

# selects first command that matches the input command
def select_command(input_command):
    for command in supported_commands:
        if input_command in command.aliases:
            return command
    return None
