import commands.appdomain_command as appdomain_cmd
import commands.exit_command as exit_cmd

supported_commands = set([
    appdomain_cmd.GetAppDomainCommand(),
    exit_cmd.ExitCommand()
])

# selects first command that matches the input command
def select_command(input_command):
    for command in supported_commands:
        if input_command in command.aliases:
            return command
    return None
