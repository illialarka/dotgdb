import commands.command as cmd

class ThreadFramesCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "thfs", "thread_frames" ]
        self.description = "Gets thread frame by thread identifier."
        self.help = "Usage: thfs <id>"

    def execute(self, agent, args):
        if len(args) == 0:
            return "Thread id is not provideded."

        thread_id = int(args[0])
        thread = agent.vm.get_thread(thread_id)
        frames = thread.get_stackframes()

        return frames

