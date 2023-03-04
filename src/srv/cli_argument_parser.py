import argparse

class CliArgumentParser(argparse.ArgumentParser):
    """
    Represents customized argument parser which does not stop
    execution after exceptions or argument parsing errors.
    """
    
    def exit(self, status: int = 0, message: str | None = None):
        # do not exit
        pass


