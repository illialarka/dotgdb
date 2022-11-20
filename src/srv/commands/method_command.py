from collections import namedtuple
from tabulate import tabulate 
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

        self._argument_parser.add_argument('-id', '--identifier', help='method identiifer', type=int, required=True)
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
            return self._get_method(agent, arguments.identifier)
        
        if arguments.subcommand == 'locations':
            return self._get_method_locations(agent, arguments.identifier)
        
        if arguments.subcommand == 'body':
            return self._get_method_body(agent, arguments.identifier)
        
        if arguments.subcommand == 'signature':
            return self._get_method_signature(agent, arguments.identifier)

        if arguments.subcommand == 'locals':
            return self._get_method_locals(agent, arguments.identifier)

    def _get_method(self, agent, method_id):
        method = agent.vm.get_method(method_id)

        return tabulate(
            [['Id:', method.id],
            ['Code Size:', method.get_code_size()],
            ['Source file path:', method.get_source_filename()],
            ['Call convention:', method.get_call_convention()],
            ['Return type:', method.get_return_type()]],
            tablefmt='simple')

    def _get_method_locations(self, agent, method_id):
        method = agent.vm.get_method(method_id)
        locations = method.get_code_locations()

        return tabulate(
            [[location.il_offset, location.line_number] for location in locations],
            tablefmt='simple',
            headers=['IL offset', 'Line Number'])
    
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
