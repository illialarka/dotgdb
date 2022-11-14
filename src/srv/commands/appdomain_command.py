import commands.command as cmd
import argparse

class AppDomainCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ 'appdomain' ]
        self.description = 'Access app domain'
        self.help = 'Usage: appdomain'

        self._argument_parser = argparse.ArgumentParser(prog='appdomain')

        self._argument_parser.add_argument('subcommand', choices=['root'], default='root', type=str)

    def execute(self, agent, args = None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return
        
        if arguments is None:
            return

        if arguments.subcommand == 'root':
            print(self._get_root_appdomain(agent))
            return
    
    def _get_root_appdomain(sefl, agent):
        return agent.vm.get_root_appdomain()
