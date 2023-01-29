import commands.command as cmd
import argparse


class ThreadsCommand(cmd.Command):
    '''
    *Temporary disabled*
    The Threads command is responsible for listing active threads. 
    '''

    def __init__(self):
        self.aliases = ['threads']
        self.description = 'Lists currently active threads in the debuggee.'
        self.help = 'Usage: threads'

        self._argument_parser = argparse.ArgumentParser(
            prog=', '.join(self.aliases),
            description=self.description)

    def execute(self, agent, args=None):
        threads = agent.vm.get_all_threads()

        return threads
