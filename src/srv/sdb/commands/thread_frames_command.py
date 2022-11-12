import commands.command as cmd
import argparse

class ThreadFramesCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "thfs", "thread_frames" ]
        self.description = "Gets thread frame by thread identifier."
        self.help = "Usage: thfs <id>"

        self._argument_parser = argparse.ArgumentParser(
                prog = ", ".join(self.aliases),
                description = self.description)

        self._argument_parser.add_argument("-id", "--identifier", help="thread identifier", type=int)

    def execute(self, agent, args = None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            pass

        if arguments is None:
            return
        
        print ('command disable due to deadlock')

        #print (agent.vm.get_thread(arguments.identifier).get_stackframes())
