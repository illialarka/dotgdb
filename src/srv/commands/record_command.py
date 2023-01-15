from commands.command import Command
from state_store_service import StateStoreService, EXECUTION_STATE_RECORDING
import logging

logger = logging.getLogger()


class RecordCommand(Command):

    def __init__(self):
        self.aliases = ['record']
        self.description = 'Runs recording and continue debugging.'
        self.help = 'Usage: record'

    def execute(self, agent, args=None, output=None):
        prompting_answer = input(
            'Running recording breakpoints will not stop execution. Are you sure? [Y/N]')

        if prompting_answer.lower() not in ['y', 'n', 'yes', 'no']:
            logger.info('Input should be Y or N.')
            return

        state_store_service = StateStoreService()
        event_descriptors = state_store_service.state.event_descriptors

        if self._any(event_descriptors, lambda item: item.event_query is not None):
            logger.info( 'Running recording.\nTo stop exeuction hit Ctrl + Z.')
            state_store_service.state.execution_state = EXECUTION_STATE_RECORDING 
            agent.vm.resume()

    def _any(self, iterable, predicate):
        for item in iterable:
            if predicate(item):
                return True

        return False

        # Well, here I should prompt a user
        # future execution will not stopped at the breakpoint
        # and will query event descriptor query and
        # save data to some temporary store
        #
        # Thinking about storage.
        # [X] In memory is good for short lived
        # data, but there is a risk to get OutOfMem error.
        # So, probably, it would be great to have some output file
        # with streaming data (applying batching).
        #
        # Thinking about visualiation.
        #
        # 1.[ ] Use built-in functions (code) to display a charts/graphs etc.
        # 2.[ ] Just save to file, for future analyzation (CSV,JSON)
        #
        # Thinking about stopping of recording.
        #
        # 1.[ ] Infinit loops - restrict with iteration/time of execution
        # 2.[ ] Just to complete the programm
        # 3.[ ] By user interruption
