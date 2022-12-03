import commands.command as cmd
import argparse
from cli_context import CliContextService

class PrintCommand(cmd.Command):
    '''
    Prints variable by name
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

    def execute(self, agent, args=None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return

        if arguments is None:
            return

        cli_context_service = CliContextService()

        if not cli_context_service.is_on_breakpoint():
            print('Can not collect stackframe because of thread when it is not on breakpoint.')
            return

        breakpoint_thread_id = cli_context_service.get_state().thread_id
        self._print_local_value(agent, breakpoint_thread_id, arguments.variable)

    def _print_local_value(self, agent, thread_id, variable):
        stackframes = agent.vm.get_thread(thread_id).get_stackframes()

        if stackframes is None or len(stackframes) == 0:
            print('Can not get stackframe for some reason.')
            return
        
        for stackframe in stackframes:
            method_locals = stackframe.get_method().get_locals()

            for method_local in method_locals:
                if method_local.name == variable:
                    print(stackframe.get_local_value(method_local))
                    return
   
        print('Could not find variable by name.')
