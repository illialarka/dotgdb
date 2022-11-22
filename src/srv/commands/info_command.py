import commands.command as cmd
import argparse

class InfoCommand(cmd.Command):

    def __init__(self):
        self.aliases = ['info']
        self.description = 'Provides information about entities.'
        self.help = 'Usage: info'

        self._argument_parser = argparse.ArgumentParser()
        self._argument_parser.add_argument('entity', help='Specifies entity info about', choices=['break'])

    def execute(self, agent, args=None):
        breakpoints = agent.breakpoints
        if len(breakpoints) == 0:
            print('There are no breakpoints')
            return

        for breakpoint in breakpoints:
            print (breakpoint)