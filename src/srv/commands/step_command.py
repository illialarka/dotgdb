from interop import event_modifiers, constants
from argparse import ArgumentParser
from state_store_service import StateStoreService
from commands.command import Command
import logging

logger = logging.getLogger()
state_store_service = StateStoreService()


class StepCommand(Command):
    '''
    The Step command is repsonsible for performing step in/over at the breakpoint.
    Could be used only on a breakpoint state.
    '''

    def __init__(self):
        self.aliases = ['step']
        self.description = 'Performs step in/over'
        self.help = 'Usage: step <in/over>'

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
        except Exception:
            return

        if arguments is None:
            return

        if state_store_service.state.event_descritor is None:
            logger.warn(
                'Can not perform step because state is not on a breakpoint.')
            return

        if arguments.type == 'in':
            self._perform_step(agent, constants.STEP_DEPTH_INTO)

        if arguments.type == 'over':
            self._perform_step(agent, constants.STEP_DEPTH_OVER)

    def _perform_step(self, agent, step_depth):
        breakpoint_thread_id = state_store_service.get_state().thread_id

        step_over_event_modifier = event_modifiers.StepModifier(
            breakpoint_thread_id, step_depth)
        agent.enable_event(
            constants.EVENT_KIND_STEP,
            constants.SUSPEND_POLICY_ALL,
            step_over_event_modifier)

        logger.info(f'Step over performed on {breakpoint_thread_id} thread.')
