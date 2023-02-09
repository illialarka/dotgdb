from commands.command import Command
from qlang.qlang_parser import parse_query
from qlang.query_interpreter import interpret
from state_store_service import StateStoreService
import argparse
import logging

logger = logging.getLogger()


class QueryCommand(Command):
    '''
    The Query command is responsible for adding QLang query to enabled breakpoints.

    Before adding the query an enabled event (breakpoint) should be added.
    See more `./qlang`.
    '''

    def __init__(self):
        self.aliases = ['query']
        self.description = 'Adds a query on breakpoint'
        self.help = 'Usage: query --request_id <breakpoint id> <QLang query>'

        self._argument_parser = argparse.ArgumentParser()
        self._argument_parser.add_argument(
            '--request_id',
            help='Specifies break point identifier',
            type=int)
        self._argument_parser.add_argument(
            'query',
            help='Specifies QLang query',
            action='store',
            type=str)

    def execute(self, agent, args=None, output=None):
        # rearrange arguments
        args = [args[0], args[1], ' '.join(args[2:])]
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return

        if arguments is None:
            return

        state_store_service = StateStoreService()
        enabled_breakpoints = state_store_service.state.event_descriptors

        breakpoint_at = None

        for breakpoint in enabled_breakpoints:
            if breakpoint.request_id == arguments.request_id:
                breakpoint_at = breakpoint

        if breakpoint_at is None:
            logger.warn(
                f'Breakpoint does not exist with identifier {arguments.request_id}.')
            return

        query_expression = None

        try:
            event_query = arguments.query.strip('\'')
            query_expression = interpret(parse_query(event_query))

            query_expression.query = event_query
        except BaseException as exception:
            logger.warn('An error occurred during the parsing query.')
            logger.error(exception)

        breakpoint_at.event_query = query_expression
        logger.info('The query has been added to the breakpoint {arguments.request_id}.')
