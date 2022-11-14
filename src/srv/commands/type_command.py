import commands.command as cmd
import argparse

class TypeCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['type']
        self.description = 'Accesses types'
        self.help = 'Usage: type -n <typename> <subcommand>'

        self._argument_parser = argparse.ArgumentParser(
            prog='type',
            description='manipulates type') 
        
        self._argument_parser.add_argument('--assembly-id', help='specifies assembly identifier', required=True, type=int)
        self._argument_parser.add_argument('--type-name', help='specifies type name', required=True, type=str)
        self._argument_parser.add_argument('subcommand', help='specifies subcommand', choices=['get', 'methods'], default='get')

    def execute(self, agent, args):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return

        if arguments.subcommand == 'get':
            print (self._get_type(agent, arguments.assembly_id, arguments.type_name))
            return

        if arguments.subcommand == 'methods':
            for method in self._get_type_methods(agent, arguments.assembly_id, arguments.type_name):
                print (method)
            return

    def _get_type(self, agent, assembly_id, type_name):
        return agent.vm.get_assembly(assembly_id).get_type_by_name(type_name)
    
    def _get_type_methods(self, agent, assembly_id, type_name):
        return agent.vm.get_assembly(assembly_id).get_type_by_name(type_name).get_methods()