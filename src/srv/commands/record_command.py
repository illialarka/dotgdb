from commands.command import Command
from state_store_service import StateStoreService, EXECUTION_STATE_RECORDING
import logging

logger = logging.getLogger()


class RecordCommand(Command):
    '''
    The Record command is responsible for starting recording of execution and collecting data.

    Important to know, it can only be terminated by LCtrl+Z.
    '''

    def __init__(self):
        self.aliases = ['record']
        self.description = 'Runs recording and continue debugging.'
        self.help = 'Usage: record'

    def execute(self, agent, args=None, output=None):
        prompting_answer = input(
            'Running recording breakpoints will not stop execution. Are you sure? [Y/N]')

        if prompting_answer.lower() not in ['y', 'n', 'yes', 'no']:
            logger.warn('Input should be Y or N.')
            return

        state_store_service = StateStoreService()
        event_descriptors = state_store_service.state.event_descriptors

        if self._any(event_descriptors, lambda item: item.event_query is not None):
            logger.info('Running recording.\nTo stop exeuction hit Ctrl + Z.')
            state_store_service.state.execution_state = EXECUTION_STATE_RECORDING
            agent.vm.resume()
        else:
            logger.info('There is no breakpoints with query')

    def _any(self, iterable, predicate):
        for item in iterable:
            if predicate(item):
                return True

        return False
