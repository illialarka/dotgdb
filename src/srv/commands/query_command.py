from commands.command import Command
from cli_context import CliContextService
from exceptions import BreakpointDoesNotExist
import argparse


class QueryCommand(Command):

    def __init__(self):
        self.aliases = ['query']
        self.description = 'Puts query on breakpoint'
        self.help = 'Usage: query -id <breakpoint id> --query <QLang query>'

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

        cli_context_service = CliContextService()
        enabled_breakpoints = cli_context_service.get_breakpoints()

        breakpoint_at = None

        for breakpoint in enabled_breakpoints:
            if breakpoint.request_id == arguments.request_id:
                breakpoint_at = breakpoint

        if breakpoint_at is None:
            raise BreakpointDoesNotExist
