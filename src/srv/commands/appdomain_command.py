import commands.command as cmd
import argparse
from tabulate import tabulate, tabulate_formats

class AppDomainCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ 'appdomain' ]
        self.description = 'Access app domain'
        self.help = 'Usage: appdomain'

        self._argument_parser = argparse.ArgumentParser(prog='appdomain')

        self._argument_parser.add_argument('subcommand', choices=['root'], default='root', nargs='?', type=str)

    def execute(self, agent, args = None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return
        
        if arguments is None:
            return

        if arguments.subcommand == 'root':
            return self._get_root_appdomain(agent)
    
    def _get_root_appdomain(sefl, agent):
        appdomain = agent.vm.get_root_appdomain()

        return tabulate(
            tablefmt='plain',
            tabular_data=
            [['Id:', appdomain.id],
             ['Full name:', appdomain.get_name()]])