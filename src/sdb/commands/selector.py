import commands.appdomain_command as appdomain

supported_commands = set([
    appdomain.GetAppDomainCommand()
])

# selects first command that matches the input command
def select_command(input_command):
    for command in supported_commands:
        if input_command in command.aliases:
            return command
    return None

