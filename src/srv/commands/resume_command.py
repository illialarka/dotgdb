from state_store_service import StateStoreService, EXECUTION_STATE_RUNNING
from commands.command import Command
import logging

logger = logging.getLogger()


class ResumeCommand(Command):
    '''
    The Resume command is responsible for resumes debugger virtual machine after hitting event.
    '''

    def __init__(self):
        self.aliases = ['resume', 'run']
        self.description = 'Runs/resumes virtual machine.'
        self.help = 'Usage: resume'

    def execute(self, agent, args=None):
        agent.vm.resume()

        state_store_service = StateStoreService()
        state_store_service.state.execution_state = EXECUTION_STATE_RUNNING

        logger.info(f'{state_store_service.state.executable_path} Resuming...')
