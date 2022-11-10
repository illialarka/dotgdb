import commands.command as cmd
import argparse

class GetAssemblyCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "get_assembly" ]
        self.description = "Gets assembly of an executable by assembly identifier."
        self.help = "Usage: get_assembly"

        self._argument_parser = argparse.ArgumentParser(
                prog = ", ".join(self.aliases),
                description = self.description)

        self._argument_parser.add_argument("-id", "--identifier", help="assembly identifier", type=int)

    def execute(self, agent, args = None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            pass

        if arguments is None:
            return

        print (agent.vm.get_assembly(arguments.identifier))
