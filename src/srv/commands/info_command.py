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

        if len(context_service.breakpoints) == 0:
            print('There are no breakpoints.')
            return

        for breakpoint in context_service.breakpoints:
            event_kind = constants.EVENT_FRIENDLY_NAME[breakpoint.event.event_kind]
            print(f'Breakpoint {breakpoint.event.request_id} kind {event_kind}.')

    def _info_locals(self):
        pass
