import commands.command as cmd
from cli_context import CliContextService

class ResumeCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['resume', 'run']
        self.description = 'Runs/resumes virtual machine.'
        self.help = 'Usage: resume'

    def execute(self, agent, args = None):
        agent.vm.resume()
        context_service = CliContextService()
        context_service.start_running_executable()
        print(f'Starting program: {context_service.get_executable()}')
        print('Use Ctrl+Z to suspend process.\n')
