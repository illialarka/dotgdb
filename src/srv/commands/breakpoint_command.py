from collections import namedtuple
from state_store_service import StateStoreService 
import commands.command as cmd
import event_modifiers
import constants
import argparse

LocationParsed = namedtuple(
    'LocationParsed',
    ['type_name', 'method_name', 'line_number'])


class BreakpointCommand(cmd.Command):
    '''
    Sets breakpoint at a location.

    Uses line number as number in original <cs> file.
    '''

    def __init__(self):
        self.aliases = ['breakpoint', 'break', 'bt']
        self.description = 'Manages breakpoints'
        self.help = 'Usage: breakpoint <action>'

        self._argument_parser = argparse.ArgumentParser()
        self._argument_parser.add_argument(
            'location',
            help=f'Sets breakpoint at specified location. Location should follow patter - <namespace.type:method:line_number>',
            type=str)

    def execute(self, agent, args=None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except BaseException:
            return

        location = self._parse_breakpoint_location(arguments.location)

        if location is None:
            print(
                'Unable to understand location you provided. Please use [-help] to get help information.')
            return

        self._set_breakpoints(
            agent,
            location.type_name,
            location.method_name,
            location.line_number)

    def _set_breakpoints(self, agent, type_name, method_name, line_number):
        assemblies = agent.vm.get_root_appdomain().get_assemblies()
        method_break_on = None
        event_request = None

        for assembly in assemblies:
            type = assembly.get_type_by_name(type_name)
            if type is None:
                continue

            method = type.get_method_by_name(method_name)
            if method is None:
                continue

            method_break_on = method

        if method_break_on is None:
            print(
                'Location to breakpoint was not found. Make sure you are at right position.')
            return

        code_locations = method_break_on.get_code_locations()

        for code_location in code_locations:
            if code_location.line_number == line_number:
                breakpoint_location = event_modifiers.LocationModifier(
                    method_break_on.id, code_location.il_offset)

                event_request = agent.enable_event(
                    constants.EVENT_KIND_BREAKPOINT,
                    constants.SUSPEND_POLICY_ALL,
                    breakpoint_location)
                break

        il_offset = code_location.il_offset
        method_file = method_break_on.get_source_filename()
        breakpoint_id = event_request.request_id

        state_store_service = StateStoreService()
        state_store_service.add_event(
            event_request, method_file, line_number, method_name)

        print(
            f'Breakpoint {breakpoint_id} has been set at 0x{il_offset:02X}: {method_file}, line {line_number}.')

    def _parse_breakpoint_location(self, location):
        parts = location.split(':')

        if len(parts) != 3:
            print(
                'Unknown location defined. Please use <type>:<method>:<linenumber> pattern.')
            return

        type_name = parts[0]
        method_name = parts[1]
        line_number = None

        try:
            line_number = int(parts[2])
        except BaseException:
            print('Unable to parse line number.')
            return

        return LocationParsed(type_name, method_name, line_number)
