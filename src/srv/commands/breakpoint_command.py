from collections import namedtuple
import commands.command as cmd
import event_modifiers
import constants
import argparse

LocationParsed = namedtuple(
    'LocationParsed',
    ['type_name', 'method_name', 'line_number'])

class BreakpointCommand(cmd.Command):

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
        except:
            return
       
        location = self._parse_breakpoint_location(arguments.location)

        if location is None:
            print('Unable to understand location you provided. Please use [-help] to get help information.')
            return

        self._set_breakpoints(agent, location.type_name, location.method_name, location.line_number)

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
            print(f'Location to breakpoint was not found. Make sure you are at right position.')
            return
        
        code_locations = method_break_on.get_code_locations()

        for code_location in code_locations:
            if code_location.line_number == line_number:
                breakpoint_location = event_modifiers.LocationModifier(method_break_on.id, code_location.il_offset) 

                event_request = agent.enable_event(
                    constants.EVENT_KIND_BREAKPOINT,
                    constants.SUSPEND_POLICY_ALL,
                    breakpoint_location)
                break 
        
        il_offset = code_location.il_offset
        method_file = method_break_on.get_source_filename() 
        breakpoint_id = event_request.request_id
        print(f'Breakpoint {breakpoint_id} has been set at 0x{il_offset:02X}: {method_file}, line {line_number}.')

    def _unset_all_breakpoints(self, agent):
        agent.disable_all_breakpoints()
    
    def _list_breakpoints(self, agent):
        breakpoints = agent.breakpoints
        print('Breakpoints list\n')
        for index in range(0, len(breakpoints)):
            breakpoint = breakpoints[index] 
            print(f'#{index} breakpoint at {breakpoint}')
    
    def _parse_breakpoint_location(self, location):
        parts = location.split(':')
        return LocationParsed(
            parts[0],
            parts[1],
            int(parts[2]) if parts[2].isdigit() else None) if len(parts) == 3 else None
