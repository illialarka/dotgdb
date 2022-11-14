import formatters.output_formatter as format

class CliOutputFormatter(format.OutputFormatter):

    def format(self, object) -> str:
        return object.__str__()