import commands.command as cmd

class ResumeCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['resume', 'run']
        self.description = 'Runs/resumes virtual machine.'
        self.help = 'Usage: resume'

    def execute(self, agent, args = None):
        agent.vm.resume()
        print('Virtual Machine resumed.')