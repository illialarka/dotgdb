from tabulate import tabulate 
from collections.abc import Sequence

class TableFormatter:
    def __init__(self):
        self._table = []
        self._header = []

    def format(self, output):
        if output is None:
            return None

        if isinstance(output, str):
            return output

        if isinstance(output, Sequence):
            for item in output:
                self._format(item)
        else:
            self._format(output)

        return tabulate(self._table, self._header)
    

    def _format(self, entity):
        dict = entity.__dict__()
        self._header = dict.keys()
        self._table.append(dict.values())