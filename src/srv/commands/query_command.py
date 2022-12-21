from commands.command import Command
from qlang.qlang_parser import parse_query
from qlang.query_interpreter import interpret
from state_store_service import StateStoreService
from exceptions import BreakpointDoesNotExist
import argparse


class QueryCommand(Command):

    def __init__(self):
        self.aliases = ['query']
        self.description = 'Puts query on breakpoint'
        self.help = 'Usage: query -id <breakpoint id> -q <QLang query>'

        self._argument_parser = argparse.ArgumentParser()
        self._argument_parser.add_argument(
            '-id',
            '--request_id',
            help='specifies break point identifier',
            type=int)
        self._argument_parser.add_argument(
            'query',
            help='specifies QLang query',
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
            raise BreakpointDoesNotExist

        query_expression = None

        try:
            event_query = arguments.query.strip('\'') 
            query_expression = interpret(parse_query(event_query))

            query_expression.query = event_query 
        except Exception as ex:
            print('produce query parsing error')
            print(ex)

        # well, technically it should work :D
        breakpoint_at.event_query = query_expression
