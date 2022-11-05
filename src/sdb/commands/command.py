class Command:

    def __init__(self):
        # fill with all possible aliases of the command
        self.aliases = []
        self.description = "No description available"
        self.help = "No help available"

    def run(self, args):
        raise NotImplementedError