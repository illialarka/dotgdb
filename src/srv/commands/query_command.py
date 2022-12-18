from commands.command import Command
from dotgdb.src.srv.qlang.qlang_parser import parse_query
from state_store_service import StateStoreService
from qlang.query_interpreter import interpret 
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
            type=str)

    def execute(self, agent, args=None, output=None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except BaseException:
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

        try:
            expression_tree = parse_query(arguments.query)
            query_expression = interpret()
        except:
            print('some error parsing and cimpiling query')

        # here we found a breakpoint and need to add a query
        # but what exectly should we add?
        # query ? - then we have to compile it every time it is executed
        # some compiled query representation ? - most likely,
        # but it requires developing those query representation context 


        # Here we shoud somehow save QLanq query
        # and to have an ability to query data on event happen
        # also, I have to decide a wayt where to store (data) results
        # of query
