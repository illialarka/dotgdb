import commands.command as cmd
import argparse
import constants
import sdbtypes
import event_modifiers

class ThreadFramesCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "thfs", "thread_frames" ]
        self.description = "Gets thread frame by thread identifier."
        self.help = "Usage: thfs <id>"

        #self._argument_parser = argparse.ArgumentParser(
        #        prog = ", ".join(self.aliases),
        #        description = self.description)

        #self._argument_parser.add_argument("-id", "--identifier", help="thread identifier", type=int)

    def execute(self, agent, args = None):
        # thfs
        e = agent.enable_event(
            constants.EVENT_KIND_BREAKPOINT,
            constants.SUSPEND_POLICY_ALL,
            event_modifiers.LocationModifier(2, 7))

        print (e)