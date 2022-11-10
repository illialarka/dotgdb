import commands.command as cmd

class GetAssemblyCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "get_assembly", "ga" ]
        self.description = "Gets assembly of an executable by assembly identifier."
        self.help = "Usage: get_assembly"

    def execute(self, agent, args = None):
        if len(args) == 0:
            print ("Assembly identifier is not provided.")

        assembly_id = int(args[0])
        print (agent.vm.get_assembly(assembly_id))
