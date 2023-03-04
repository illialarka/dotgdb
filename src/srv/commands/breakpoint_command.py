from collections import namedtuple
from state_store_service import StateStoreService
from interop import event_modifiers, constants
from commands.command import Command
from cli_argument_parser import CliArgumentParser

import logging
import argparse

LocationParsed = namedtuple(
    "LocationParsed",
    ["type_name", "method_name", "line_number"])

logger = logging.getLogger()

# FIXME: Add descriptive doc how it parses and uses arguments 
class BreakpointCommand(Command):
    """
    The Breakpoint command is responsible for placing breakpoint events at the specific line of source code.

    Pattern:

        breakpoint <namespace>.<type_name>:<method_name>:<line_number>
        breakpoint <full_source_file_path>:<line_number>

    Example source code:

    Utils.cs
    ```
    1   namesapce Utils:
    2
    3    public class Utils
    4    {
    5        public int Add(int first, int second)
    6        {
    7           var result = first + second;
    8
    9           return result;
    10       }
    11    }
    ```

    To place a breakpoint at the 8th line, use: 

        `breakpoint Utils.Util:Add:9`
    
    or

        `breakpoint /src/Utils.cs:9`

    """

    def __init__(self):
        self.aliases = ["breakpoint", "break", "bt"]
        self.description = "Manages breakpoints"
        self.help = """Usage: 
            breakpoint <namespace>.<type_name>:<method_name>:<line_number> or
            breakpoint <source_file_path>:<line_number>
            """
        self.scopes = ["breakpoints"]

        self._argument_parser = CliArgumentParser(
            prog="breakpoints",
            usage=self.help)

        type_arguments_group = self._argument_parser.add_argument_group("type")

        type_arguments_group.add_argument(
            "-n",
            "--namespace",
            help="Specifies desired type namespace",
            type=str,
            required=True)

        type_arguments_group.add_argument(
            "-t",
            "--type",
            help="Specifies desired type name",
            type=str,
            required=True) 

        type_arguments_group.add_argument(
            "-m",
            "--method",
            help="Specifies desired method name",
            type=str,
            required=True)

        file_arguments_group = self._argument_parser.add_argument_group("file")

        file_arguments_group.add_argument(
            "-f",
            "--file",
            help="Specifies desired file name",
            type=str,
            required=True)

        self._argument_parser.add_argument(
            "-l",
            "--line",
            help="Specifies desired line number name",
            type=int,
            required=True)


    def execute(self, agent, args=None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except Exception:
            return

        print(arguments)

        location = self._parse_breakpoint_location(arguments.location)

        if location is None:
            logger.warn(
                "Unable to understand specified code location. Please use [-help] to get help information.")
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
            print(method.get_source_filename())
            if method is None:
                continue

            method_break_on = method

        if method_break_on is None:
            logger.warn(
                "Location was not found. Make sure you are at right location.")
            return

        code_location = None
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

        if code_location is None or event_request is None:
            logger.info("Could not find code location.")
            return

        il_offset = code_location.il_offset
        method_file = method_break_on.get_source_filename()
        breakpoint_id = event_request.request_id

        state_store_service = StateStoreService()
        state_store_service.add_event(
            event_request, method_file, line_number, method_name)

        logger.info(
            f"Breakpoint {breakpoint_id} has been set at 0x{il_offset:02X}: {method_file}, line {line_number}.")

    def _parse_breakpoint_location(self, location):
        parts = location.split(":")

        if len(parts) != 3:
            logger.warn(
                "Unknown location defined. Please use <type>:<method>:<linenumber> pattern.")
            return

        type_name = parts[0]
        method_name = parts[1]
        line_number = None

        try:
            line_number = int(parts[2])
        except BaseException:
            logger.warn("Unable to parse line number.")
            return

        return LocationParsed(type_name, method_name, line_number)
