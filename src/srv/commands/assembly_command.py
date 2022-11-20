import commands.command as cmd
import argparse
from tabulate import tabulate

class AssemblyCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ 'assembly' ]
        self.description = 'Gets assembly by identifier.'
        self.help = 'Usage: assembly -id=<assembly_id> [action]'

        self._argument_parser = argparse.ArgumentParser(
                prog = ', '.join(self.aliases),
                description = self.description)

        self._argument_parser.add_argument('-id', '--identifier', help='assembly identiifer', type=int, required=True)
        self._argument_parser.add_argument('subcommand', choices=['get', 'entry', 'object', 'manifest'], default='get', type=str, nargs='?')

    def execute(self, agent, args):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return

        if arguments.subcommand == 'get':
            return self._get_assembly(agent, arguments.identifier)
        
        if arguments.subcommand == 'entry':
            return self._get_assembly_entry(agent, arguments.identifier)

        if arguments.subcommand == 'object':
            return self._get_assembly_object(agent, arguments.identifier)

        if arguments.subcommand == 'manifest':
            return self._get_assembly_manifest(agent, arguments.identifier)
        
    def _get_assembly(self, agent, assembly_id):
        assembly =  agent.vm.get_assembly(assembly_id)

        return tabulate(
            [['Id', assembly.id],
             ['Name', assembly.get_name()]],
            tablefmt='simple') 

    def _get_assembly_entry(self, agent, assembly_id):
        entry = agent.vm.get_assembly(assembly_id).get_entry_point() 

        return tabulate(
            [['Id', entry.id],
             ['Entry', entry.get_name()],
             ['Code size', entry.get_code_size()],
             ['Source file path', entry.get_source_filename()]],
            tablefmt='simple')
 
    def _get_assembly_object(self, agent, assembly_id):
        object = agent.vm.get_assembly(assembly_id).get_object() 

        return tabulate(
            [['Id', object.id],
            ['Name', object.get_type()],
            ['Address', object.get_address()],
            ['Collected', object.get_is_collected()]],
            tablefmt='simple')

    def _get_assembly_manifest(self, agent, assembly_id):
        manifest = agent.vm.get_assembly(assembly_id).get_manifest_module() 

        return tabulate(
            [['Id', manifest.id],
            ['Basename', manifest.get_basename()],
            ['Scopename', manifest.get_scopename()]],
            tablefmt='plain')