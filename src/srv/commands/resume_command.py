from state_store_service import StateStoreService, EXECUTION_STATE_RUNNING
import commands.command as cmd


class ResumeCommand(cmd.Command):
    '''
    Resumes debugger virtual machine.

    Runs or resumes actual debugger execution of thread.
    '''

    def __init__(self):
        self.aliases = ['resume', 'run']
        self.description = 'Runs/resumes virtual machine.'
        self.help = 'Usage: resume'

    def execute(self, agent, args=None):
        agent.vm.resume()

        state_store_service = StateStoreService()
        state_store_service.state.execution_state = EXECUTION_STATE_RUNNING

        print(f'Starting program: {state_store_service.state.executable_path}')
        print('Use Ctrl+Z to suspend process.\n')
