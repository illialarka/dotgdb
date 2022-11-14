import commands.command as cmd
import argparse

class MethodCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['method']
        self.description = 'Access method'
        self.help = 'Usage: method'

        self._argument_parser = argparse.ArgumentParser(prog='method') 

        self._argument_parser.add_argument('--method-id', help='specifies methods identifier', required=True, type=int)
        self._argument_parser.add_argument('subcommand', help='specifies subcomand', choices=['get', 'locations'], default='get')
    
    def execute(self, agent, args):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return
        
        print(arguments)

        if arguments is None:
            return

        if arguments.subcommand == 'get':
            print(self._get_method(agent, arguments.method_id))
            return
        
        if arguments.subcommand == 'locations':
            for location in self._get_method_locations(agent, arguments.method_id):
                print(location)
            return

    def _get_method(self, agent, method_id):
        return agent.vm.get_method(method_id)

    def _get_method_locations(self, agent, method_id):
        return agent.vm.get_method(method_id).get_code_locations()