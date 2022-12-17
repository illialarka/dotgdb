import commands.command as cmd
import argparse
from state_store_service import StateStoreService 

state_store_service = StateStoreService()


class ThreadStackframeCommand(cmd.Command):
    '''
    Manages thread stackframes.

    Based on the subcommand, applies different logic.

    'stackcall' (default) - displays the call stack.
    'locals' - displays all local variables in the thread of execution.
    '''

    def __init__(self):
        self.aliases = ['stackframe']
        self.description = 'Gets tackframe information'
        self.help = 'Ussage: stackframe'

        self._argument_parser = argparse.ArgumentParser()
        self._argument_parser.add_argument(
            '-id',
            '--thread-id',
            help='sepcifies thread identifier',
            type=int,
        )

        self._argument_parser.add_argument(
            'subcommand',
            help='specifies subcommand',
            choices=['stackcall', 'locals'],
            default='stackcall',
            type=str,
            nargs='?')

    def execute(self, agent, args=None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except BaseException:
            return

        if arguments is None:
            return

        if state_store_service.state.event_descritor is None:
            print(
                'Can not collect stackframe because of thread when it is not on breakpoint.')
            return

        breakpoint_thread_id = state_store_service.state.event_descritor.thread_id

        if arguments.subcommand == 'stackcall':
            self._get_stackcall(agent, breakpoint_thread_id)
            return

        if arguments.subcommand == 'locals':
            self._get_locals(agent, breakpoint_thread_id)
            return

    def _get_stackcall(self, agent, identifier):

        stackframes = agent.vm.get_thread(identifier).get_stackframes()

        if stackframes is None or len(stackframes) == 0:
            print('Can not get stackframe for some reason.')
            return

        print('Stackframe call tree:\n')

        for stackframe in stackframes:
            parameters_names = stackframe.get_method().get_params()
            stackframe_formated = stackframe.__str__()

            for parameter_name in parameters_names:
                stackframe_formated = stackframe_formated + \
                    f'<{parameter_name.name}>'
            print(stackframe_formated)

        return

    def _get_locals(self, agent, identifier):
        stackframes = agent.vm.get_thread(identifier).get_stackframes()

        if stackframes is None or len(stackframes) == 0:
            print('Can not get stackframe for some reason.')
            return

        for stackframe in stackframes:
            method_locals = stackframe.get_method().get_locals()

            for method_local in method_locals:
                print(f'<${method_local.name}> at {stackframe}')

        return
