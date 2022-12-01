import commands.command as cmd
import argparse

class PrintCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['print']
        self.description = 'Prints variable. Used only at breakpoint state.'
        self.help = 'Usage: print <variable_name>'

        self._argument_parser = argparse.ArgumentParser() 
        self._argument_parser.add_argument(
            'variable',
            help='displays value of the variable',
            type=str)

        self._argument_parser.add_argument(
            '-id',
            '--thread-id',
            help='specifies thread identifier',
            type=str,
            required=True)

    def execute(self, agent, args=None):
        arguments = None
        try:
            arguments = self._argument_parser.parser_args(args)
        except:
            return
        
        if arguments is None:
            return

        context_service = CliContextService()

        if not context_service.is_on_breakpoint():
            print('Can not collect stackframe because of thread when it is not on breakpoint.')
            return

        stackframes = agent.vm.get_thread(identifier).get_stackframes()

        if stackframes is None or len(stackframes) == 0:
            print('Can not get stackframe for some reason.')
            return
        
        for stackframe in stackframes:
            variable =  stackframe.get_local_value(arguments.variable)
            print(varialbe)
            if variable is not None:
                print(variable)
                return
    
        print('Could not find variable by name.')
 
