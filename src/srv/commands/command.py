class Command:

    def __init__(self):
        self.aliases = []
        self.description = "No description available"
        self.help = "No help available"
        self.subcommands = []

    def execute(self, agent, args = None):
        raise NotImplementedError