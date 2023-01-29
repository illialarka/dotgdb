from commands.command import Command
from state_store_service import StateStoreService
import argparse
import logging

logger = logging.getLogger()


class PrintCommand(Command):
    '''
    The Print command is responsible for printing variable by name.

    By default, it uses the identifier of the thread on which the break event occurred.
    To print variable from another thread use <thread-id> parameter to specify thread.
    '''

    def __init__(self):
        self.aliases = ['print']
        self.description = 'Prints variable. Used only at breakpoint state.'
        self.help = 'Usage: print <variable_name>'

        self._argument_parser = argparse.ArgumentParser()
        self._argument_parser.add_argument(
            'variable',
            help='displays value of the variable',
            type=str,
            nargs='?')

        self._argument_parser.add_argument(
            '--thread-id',
            help='specifies thread identifier',
            type=int,
            nargs='?')

    def execute(self, agent, args=None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except BaseException:
            return

        if arguments is None:
            return

        state_store_service = StateStoreService()

        if state_store_service.state.event_descritor is None:
            logger.warn(
                'Can not collect stackframe of thread because state is not at breakpoint.')
            return

        breakpoint_thread_id = state_store_service.state.event_descritor.thread_id
        self._print_local_value(
            agent,
            breakpoint_thread_id,
            arguments.variable)

    def _print_local_value(self, agent, thread_id, variable):
        stackframes = agent.vm.get_thread(thread_id).get_stackframes()

        if stackframes is None or len(stackframes) == 0:
            logger.warn('Can not get stackframe for some reason.')
            return

        for stackframe in stackframes:
            method_locals = stackframe.get_method().get_locals()

            for method_local in method_locals:
                if method_local.name == variable:
                    logger.info(stackframe.get_local_value(method_local))
                    return

        logger.warn('Could not find variable by name.')
