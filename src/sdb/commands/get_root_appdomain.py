import commands.command as cmd

class GetAppDomainCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "appdomain", "getappdomain", "gad" ]
        self.description = "Get the application domain name of an executable."
        self.help = "Usage: appdomain"

    def execute(self, agent, args = None):
        print (agent.vm.get_root_appdomain())
