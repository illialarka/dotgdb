import formatters.output_formatter as format
import json

class JsonOutputFormatter(format.OutputFormatter):

    def format(self, object) -> str:
        return json.dumps(obj=object.__dict__(), indent=4)