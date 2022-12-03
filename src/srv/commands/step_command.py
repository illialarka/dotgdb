from event_modifiers import StepOverModifier
from cli_context import CliContextService
import commands.command as cmd
import constants


class StepCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['step']
        self.description = 'Performs step in/over'
        self.help = 'Usage: step'

    def execute(self, agent, args=None):
        self._step_over(agent)

    def _step_over(self, agent):
        cli_context_service = CliContextService()

        breakpoint_thread_id = cli_context_service.get_state().thread_id
        print(f'thread id = {breakpoint_thread_id}')

        step_over_event_modifier = StepOverModifier(breakpoint_thread_id)
        agent.enable_event(
            constants.EVENT_KIND_STEP,
            constants.SUSPEND_POLICY_ALL,
            step_over_event_modifier)

        print(f'Step over performed on {breakpoint_thread_id} thread.')
