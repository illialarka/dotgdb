import commands.command as cmd
import commands.selector as selector
import logging

logger = logging.getLogger()


class SupportedCommands(cmd.Command):

    def __init__(self):
        self.aliases = ['help', 'supported', 'supportedcommands', 'sc']
        self.description = 'Lists all supported commands.'
        self.help = 'Usage: supported_commands'

    def execute(self, agent, args=None):
        supported_commands = selector.supported_commands

        for command in supported_commands:
            print(', '.join(command.aliases) + ' - ' + command.description)
            print(command.help.rjust(len(command.help) + 4, ' '))
            print()
