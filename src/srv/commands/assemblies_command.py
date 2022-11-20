import commands.command as cmd
import argparse
from tabulate import tabulate

class AssembliesCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "assemblies" ]
        self.description = "Gets assemblies of an executable."
        self.help = "Usage: get_assemblies"

        self._argument_parser = argparse.ArgumentParser(
                prog = ", ".join(self.aliases),
                description = self.description)

    def execute(self, agent, _ = None):
        return self._format_assemblies(agent.vm.get_root_appdomain().get_assemblies())
    
    def _format_assemblies(self, assemblies):
        return tabulate(
            tabular_data=[[assembly.id, assembly.get_name()] for assembly in assemblies],
            headers=['Id', 'Name'])