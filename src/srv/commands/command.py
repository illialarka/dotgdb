class Command:

    def __init__(self):
        self.aliases = []
        self.description = "No description available"
        self.help = "No help available"

    def execute(self, agent, args=None, writer=None):
        raise NotImplementedError
