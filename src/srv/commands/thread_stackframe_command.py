import commands.command as cmd

class ThreadStackframeCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['stackframe']
        self.description = 'Gets tackframe'
        self.help = 'Ussage: stackframe'
    
    def execute(self, agent, args=None):
        pass