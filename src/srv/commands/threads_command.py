import commands.command as cmd
import argparse
import constants

class ThreadsCommand(cmd.Command):
    def __init__(self):
        self.aliases = [ "threads", "ths" ]
        self.description = "Lists all threads in the process."
        self.help = "Usage: threads"

        self._argument_parser = argparse.ArgumentParser(
                prog = ", ".join(self.aliases),
                description = self.description)

    def execute(self, agent, args = None):
        for m in agent.vm.get_assembly(2).get_type_by_name("Utils.Util").get_methods():
            print (m)
