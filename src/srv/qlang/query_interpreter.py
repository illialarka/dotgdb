from lark.visitors import Interpreter
from source_interpreter import SourceClauseInterpreter
from select_interpreter import SelectClauseInterpreter

import logging

logger = logging.getLogger()


class QueryInterpreter(Interpreter):

    def __init__(self, agent, context):
        self._agent = agent
        self._context = context

    def source(self, source_node):
        SourceClauseInterpreter(self._agent, self._context).visit(source_node)

    def condition_clause(self, _):
        print(f'Filtering data set by condition.')

    def select_clause(self, select_clause_node):
        SelectClauseInterpreter(self._context).visit(select_clause_node)


class QueryContext:

    def __init__(self):
        self.data = []
        self.projections = []

    def execute(self):
        projected_data = []

        for data_item in self.data:
            projected_item = {}

            for projection in self._context.projections:
                if projection in data_item:
                    projected_item[projection] = data_item[projection]
                    continue
                else:
                    projected_item[projection] = None
            projected_data.append(projected_item)

        return projected_data


def interpret(root):
    query_context = QueryContext()
    QueryInterpreter(query_context).visit(root)

    return query_context.execute()
