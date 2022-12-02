import commands.command as cmd
import argparse
from cli_context import CliContextService

class PrintCommand(cmd.Command):

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
            required=True)

    def execute(self, agent, args=None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            return

        if arguments is None:
            return

        context_service = CliContextService()

        if not context_service.is_on_breakpoint():
            print('Can not collect stackframe because of thread when it is not on breakpoint.')
            return

        stackframes = agent.vm.get_thread(arguments.thread_id).get_stackframes()

        if stackframes is None or len(stackframes) == 0:
            print('Can not get stackframe for some reason.')
            return
        
        for stackframe in stackframes:
            method_locals = stackframe.get_method().get_locals()

            for method_local in method_locals:
                if method_local.name == arguments.variable:
                    print(stackframe.get_local_value(method_local))
                    return
   
        print('Could not find variable by name.')
