from collections import namedtuple
import commands.command as cmd
import argparse

MethodSignature = namedtuple(
    "MethodSignature",
    ["return_type", "method_name", "parameters"])

class MethodCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['method']
        self.description = 'Access method'
        self.help = 'Usage: method'

        self._argument_parser = argparse.ArgumentParser(prog='method') 

        self._argument_parser.add_argument('--method-id', help='specifies methods identifier', required=True, type=int)
        self._argument_parser.add_argument(
            'subcommand',
            help='specifies subcomand',
            choices=['get', 'locations', 'body', 'signature', 'locals'],
            default='get',
            type=str,
            nargs='?')
 
    def execute(self, agent, args):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return
        
        if arguments is None:
            return

        if arguments.subcommand == 'get':
            print(self._get_method(agent, arguments.method_id))
            return
        
        if arguments.subcommand == 'locations':
            for location in self._get_method_locations(agent, arguments.method_id):
                print(location)
            return
        
        if arguments.subcommand == 'body':
            print(self._get_method_body(agent, arguments.method_id))
            return
        
        if arguments.subcommand == 'signature':
            print(self._get_method_signature(agent, arguments.method_id))
            return

        if arguments.subcommand == 'locals':
            print(self._get_method_locals(agent, arguments.method_id))
            return

    def _get_method(self, agent, method_id):
        return agent.vm.get_method(method_id)

    def _get_method_locations(self, agent, method_id):
        return agent.vm.get_method(method_id).get_code_locations()
    
    def _get_method_body(self, agent, method_id):
        return agent.vm.get_method(method_id).get_body()
    
    def _get_method_signature(self, agent, method_id):
        method = agent.vm.get_method(method_id)

        return_type = method.get_return_type()
        method_name = method.get_name()
        parameters = method.get_params()

        return MethodSignature(return_type, method_name, parameters)

    def _get_method_locals(self, agent, method_id):
        return agent.vm.get_method(method_id).get_locals()
