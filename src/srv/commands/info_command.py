import commands.command as cmd
from cli_context import CliContextService 
import argparse
import constants

class InfoCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['info']
        self.description = 'Provides information about entities.'
        self.help = 'Usage: info'

        self._argument_parser = argparse.ArgumentParser()
        self._argument_parser.add_argument('entity', help='Specifies entity info about', choices=['break', 'locals'])

    def execute(self, agent, args=None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return

        if arguments is None:
            return
        
        if arguments.entity == 'break':
            self._info_breakpoints()
            return

    def _info_breakpoints(self):
        context_service = CliContextService()

        if len(context_service.get_breakpoints()) == 0:
            print('There are no breakpoints.')
            return

        for breakpoint in context_service.get_breakpoints():
            # would be great to have a file name also 
            print(f'Breakpoint {breakpoint.request_id} kind {breakpoint.friendly_event_kind_name} at {breakpoint.source}:{breakpoint.line_number:08X}.')

    def _info_locals(self):
        pass
