import commands.command as cmd
import argparse

class ThreadsCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['threads']
        self.description = 'Lists all threads in the process.'
        self.help = 'Usage: threads'

        self._argument_parser = argparse.ArgumentParser(
                prog = ', '.join(self.aliases),
                description = self.description)

    def execute(self, agent, args = None):
        for thread in agent.vm.get_all_threads():
            print(thread)
