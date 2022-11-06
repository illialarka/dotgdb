import commands.appdomain_command as appdomain_cmd
import commands.exit_command as exit_cmd
import commands.supported_commands as supported_cmd
import commands.threads_command as threads_cmd

supported_commands = set([
    appdomain_cmd.GetAppDomainCommand(),
    exit_cmd.ExitCommand(),
    supported_cmd.SupportedCommands(),
    threads_cmd.ThreadsCommand()
])

# selects first command that matches the input command
def select_command(input_command):
    for command in supported_commands:
        if input_command in command.aliases:
            return command
    return None
