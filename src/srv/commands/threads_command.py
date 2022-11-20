import commands.command as cmd
import argparse
from tabulate import tabulate

class ThreadsCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['threads']
        self.description = 'Lists all threads in the process.'
        self.help = 'Usage: threads'

        self._argument_parser = argparse.ArgumentParser(
                prog = ', '.join(self.aliases),
                description = self.description)

    def execute(self, agent, args = None):
        threads = agent.vm.get_all_threads()

        return tabulate(
            [[thread.id, thread.get_name(), thread.get_is_from_threadpool(), thread.get_state()] for thread in threads],
            headers=['id', 'name', 'is from pool', 'state'])