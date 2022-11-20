import commands.command as cmd
import argparse
import sys
from tabulate import tabulate

class AssembliesCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "assemblies" ]
        self.description = "Gets assemblies of an executable."
        self.help = "Usage: get_assemblies"

        self._argument_parser = argparse.ArgumentParser(
                prog = ", ".join(self.aliases),
                description = self.description)

    def execute(self, agent, _ = None, output = None):
        return self._format_output(output, agent.vm.get_root_appdomain().get_assemblies())
    
    def _format_output(self, out, assemblies):
        if out is None:
            out = sys.stdout 

        return tabulate(
            [[assembly.id, assembly.get_name()] for assembly in assemblies],
            headers=['Id', 'Name'])