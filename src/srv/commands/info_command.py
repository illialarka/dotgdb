from state_store_service import StateStoreService
from commands.command import Command
import argparse


class InfoCommand(Command):
    '''
    Provides information about debuggee entities.

    Entities:
        <break> - shows breakpoints information 
    '''

    def __init__(self):
        self.aliases = ['info']
        self.description = 'Provides information about entities.'
        self.help = 'Usage: info'

        self._argument_parser = argparse.ArgumentParser()
        self._argument_parser.add_argument(
            'entity', help='Specifies entity info about', choices=['break'])

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
        state_store_service = StateStoreService()
        event_descriptors = state_store_service.state.event_descriptors

        if len(event_descriptors) == 0:
            print('There are no breakpoints.')
            return

        for breakpoint in event_descriptors:
            print(f'Breakpoint {breakpoint.request_id} kind {breakpoint.friendly_event_kind_name} in {breakpoint.method_name}() at {breakpoint.source}:{breakpoint.line_number}.')

            if breakpoint.query is not None:
                print(
                    '@@ event query @@',
                    f'+ \t {breakpoint.query.query}',
                    sep='\n')

    def _info_locals(self):
        pass
