import commands.command as cmd
import argparse
from cli_context import CliContextService

class ThreadStackframeCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['stackframe']
        self.description = 'Gets tackframe'
        self.help = 'Ussage: stackframe'

        self._argument_parser = argparse.ArgumentParser()
        self._argument_parser.add_argument(
            '-id',
            '--identifier',
            help='sepcifies thread identifier',
            type=int,
            required=True)
        
        self._argument_parser.add_argument(
            'subcommand',
            help='specifies subcommand',
            choices=['stackcall'],
            default='stackcall',
            type=str,
            nargs='?')

    def execute(self, agent, args=None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return

        if arguments is None:
            return

        if arguments.subcommand == 'stackcall':
            self._get_locals(agent, arguments.identifier)
            return

    def _get_locals(self, agent, identifier):
        context_service = CliContextService()

        if not context_service.is_on_breakpoint():
            print('Can not collect stackframe because of thread when it is not on breakpoint.')
            return

        stackframes = agent.vm.get_thread(identifier).get_stackframes()

        if stackframes is None or len(stackframes) == 0:
            print('Can not get stackframe for some reason.')
            return

        print('Stackframe call tree:\n')
        for stackframe in stackframes:
            print(stackframe)

        return
