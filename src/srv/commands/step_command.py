from event_modifiers import StepOverModifier
from argparse import ArgumentParser
from cli_context import CliContextService
import commands.command as cmd
import constants

cli_context_service = CliContextService()


class StepCommand(cmd.Command):
    '''
    Performs step in/over at the breakpoint.
    Could be used only on a breakpoint state.
    '''

    def __init__(self):
        self.aliases = ['step']
        self.description = 'Performs step in/over'
        self.help = 'Usage: step'

        self._argument_parser = ArgumentParser()
        self._argument_parser.add_argument(
            'type',
            help='specifies type of step (in/over)',
            choices=['in', 'over'],
            default='over',
            type=str,
            nargs='?')

    def execute(self, agent, args=None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except BaseException:
            return

        if arguments is None:
            return

        if not cli_context_service.is_on_breakpoint():
            print(
                'Can not performe step because state is not on a breakpoint.')
            return

        if arguments.type == 'in':
            print('Step in is not implemented yet')

        if arguments.type == 'over':
            self._step_over(agent)

    def _step_over(self, agent):
        cli_context_service = CliContextService()
        breakpoint_thread_id = cli_context_service.get_state().thread_id

        step_over_event_modifier = StepOverModifier(breakpoint_thread_id)
        agent.enable_event(
            constants.EVENT_KIND_STEP,
            constants.SUSPEND_POLICY_ALL,
            step_over_event_modifier)

        print(f'Step over performed on {breakpoint_thread_id} thread.')
