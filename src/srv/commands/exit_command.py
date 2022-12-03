import commands.command as cmd
import exceptions as exceptions


class ExitCommand(cmd.Command):
    '''
    Exists SDB CLI process.
    '''

    def __init__(self):
        self.aliases = ["exit"]
        self.description = "Exitst the debugger client and kills processes."
        self.help = "Usage: exit"

    def execute(self, agent=None, args=None):
        raise exceptions.ExitException()
