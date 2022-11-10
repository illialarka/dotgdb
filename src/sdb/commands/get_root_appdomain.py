import commands.command as cmd

class GetAppDomainCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "appdomain", "getappdomain", "gad" ]
        self.description = "Get the application domain name of an executable."
        self.help = "Usage: appdomain"

    def register_subparser(self, parser):
        pass

    def execute(self, agent, args = None):
        return agent.vm.get_root_appdomain().get_name()
