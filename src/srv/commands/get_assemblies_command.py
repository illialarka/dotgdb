import commands.command as cmd
import argparse

class GetAssembliesCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "get_assemblies", "gas" ]
        self.description = "Gets assemblies of an executable."
        self.help = "Usage: get_assemblies"

        self._argument_parser = argparse.ArgumentParser(
                prog = ", ".join(self.aliases),
                description = self.description)

    def execute(self, agent, args = None):
        counter = 0
        for assembly in agent.vm.get_root_appdomain().get_assemblies():
            print ("#{0} {1}".format(counter, assembly))
            counter += 1
