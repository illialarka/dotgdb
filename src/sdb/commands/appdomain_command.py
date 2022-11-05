import commands.command as cmd

class GetAppDomainCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "appdomain", "getappdomain", "gad" ]
        self.description = "Get the application domain name of an executable."
        self.help = "Usage: appdomain"

    def execute(self, vm, args):
        # ignores args
        return vm.get_root_appdomain().get_name()
