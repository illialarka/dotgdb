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
            [[assembly.id, assembly.get_name()]],
            headers=['id', 'name']) 

    def _get_assembly_entry(self, agent, assembly_id):
        entry = agent.vm.get_assembly(assembly_id).get_entry_point() 

        return tabulate(
            [[entry.id, entry.get_name(), entry.get_code_size(), entry.get_source_filename()]],
            headers=['id', 'name', 'size', 'source'])
 
    def _get_assembly_object(self, agent, assembly_id):
        object = agent.vm.get_assembly(assembly_id).get_object() 

        return tabulate(
            [[object.id, object.get_type(), object.get_address()]],
            headers=['id', 'type', 'address'])

    def _get_assembly_manifest(self, agent, assembly_id):
        manifest = agent.vm.get_assembly(assembly_id).get_manifest_module() 

        return tabulate(
            [[manifest.id, manifest.get_basename(), manifest.get_scopename()]],
            headers=['id', 'basename', 'scopename'])