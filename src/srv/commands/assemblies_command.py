import commands.command as cmd
import argparse

class AssembliesCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "assemblies" ]
        self.description = "Gets assemblies of an executable."
        self.help = "Usage: get_assemblies"

        self._argument_parser = argparse.ArgumentParser(
                prog = ", ".join(self.aliases),
                description = self.description)

    def execute(self, agent, _ = None):
        for assembly in agent.vm.get_root_appdomain().get_assemblies():
            print (assembly)