import commands.command as cmd
import argparse
import assembly_mirror
import method_mirror

class AssemblyCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ 'assembly' ]
        self.description = 'Gets assembly by identifier.'
        self.help = 'Usage: assembly -id=<assembly_id> [action]'

        self._argument_parser = argparse.ArgumentParser(
                prog = ', '.join(self.aliases),
                description = self.description)

        self._argument_parser.add_argument('-id', '--identifier', help='assembly identiifer', type=int, required=True)
        self._argument_parser.add_argument('subcommand', choices=['get', 'entry', 'object'], default='get', type=str)

    def execute(self, agent, args):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return

        if arguments.subcommand == 'get':
            print(self._get_assembly(agent, arguments.identifier))
            return
        
        if arguments.subcommand == 'entry':
            print(self._get_assembly_entry(agent, arguments.identifier))
            return
        
    def _get_assembly(self, agent, assembly_id) -> assembly_mirror.AssemblyMirror:
        return agent.vm.get_assembly(assembly_id)

    def _get_assembly_entry(self, agent, assembly_id) -> method_mirror.MethodMirror: 
        return agent.vm.get_assembly(assembly_id).get_entry_point() 