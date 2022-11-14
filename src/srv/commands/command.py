class Command:

    def __init__(self):
        self.aliases = []
        self.description = "No description available"
        self.help = "No help available"
        self.subcommands = []

    def execute(self, agent, args = None):
        raise NotImplementedError

    def select_subcommand(self, command_name:str):
        for subcommand in self.subcommands:
            if command_name in subcommand.aliases:
                return subcommand
        return None
