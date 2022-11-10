import commands.command as cmd

class GetAssembliesCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "get_assemblies", "gas" ]
        self.description = "Gets assemblies of an executable."
        self.help = "Usage: get_assemblies"

    def execute(self, agent, args = None):
        for assembly in agent.vm.get_root_appdomain().get_assemblies():
            print (assembly)
