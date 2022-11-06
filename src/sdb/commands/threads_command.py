import commands.command as cmd

class ThreadsCommand(cmd.Command):
    def __init__(self):
        self.aliases = [ "threads", "ths" ]
        self.description = "Lists all threads in the process."
        self.help = "Usage: threads"

    def execute(self, agent, args = None):
        threads = agent.vm.get_all_threads()
        for thread in threads:
            print (thread.get_name())