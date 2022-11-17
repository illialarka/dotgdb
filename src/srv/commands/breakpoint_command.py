import commands.command as cmd
import event_modifiers
import constants
import argparse

class BreakpointCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['breakpoint', 'bt']
        self.description = 'Manages breakpoints'
        self.help = 'Usage: breakpoint <action>'

        self._argument_parser = argparse.ArgumentParser() 

        self._argument_parser.add_argument(
            'subcommand',
            choices=['set', 'list', 'remove', 'unsetall'],
            default='get',
            type=str,
            nargs='?')

        self._argument_parser.add_argument('--method-id', help='specifies breakpoint method indentifier', type=int)
        self._argument_parser.add_argument('--il-offset', help='specifies breakpoint method offset', type=int)

    def execute(self, agent, args=None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return

        if arguments is None:
            return

        if arguments.subcommand == 'list':
            pass

        if arguments.subcommand == 'set':
            if arguments.method_id is None or arguments.il_offset is None:
                print("Method id and IL offset should be specified")
                return

            event_request = self._set_breakpoints(
                agent,
                event_modifiers.LocationModifier(arguments.method_id, arguments.il_offset))
            print("Breakpoint is set. Event request {0}".format(event_request))

        if arguments.subcommand == 'remove':
            pass

        if arguments.subcommand == 'unsetall':
            pass

    def _set_breakpoints(self, agent, location):
        return agent.enable_event(
            constants.EVENT_KIND_BREAKPOINT,
            constants.SUSPEND_POLICY_ALL,
            location)

    def _unset_all_breakpoints(self, agent):
        agent.disable_all_breakpoints()
