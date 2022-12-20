from commands.command import Command

class RecordCommand(Command):

    def __init__(self):
        self.aliases = ['record']
        self.description = 'Runs recording and continue debugging.'
        self.help = 'Usage: record'
    
    def execute(self, agent, args=None, output=None):
        pass
        # Well, here I should prompt a user
        # future execution will not stopped at the breakpoint
        # and will query event descriptor query and 
        # save data to some temporary store
        # 
        # Thinking about storage, in memory is good for short lived 
        # data, but there is a risk to get OutOfMem error.
        # So, probably, it would be great to have some output file 
        # with streaming data (applying batching). 
        #
        # Thinking about visualiation.
        # 
        # 1. Use built-in functions (code) to display a charts/graphs etc.
        # 2. Just save to file, for future analyzation (CSV,JSON) 
        # 
        # Thinking about stopping of recording.
        # 
        # 1. Infinit loops - restrict with iteration/time of execution
        # 2. Just to complete the programm 
        # 3. By user interruption
        #  