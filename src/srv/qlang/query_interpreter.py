from lark.visitors import Interpreter
from qlang.source_clause_interpreter import SourceClauseInterpreter
from qlang.select_interpreter import SelectClauseInterpreter
from qlang.query_expression import QueryExpression

import logging

logger = logging.getLogger()


class QueryInterpreter(Interpreter):

    def __init__(self):
        self.expression = QueryExpression()

    def source(self, source_node):
        SourceClauseInterpreter(self.expression).visit(source_node)

    def condition_clause(self, _):
        print(f'Filtering data set by condition.')

    def select_clause(self, select_clause_node):
        SelectClauseInterpreter(self.expression).visit(select_clause_node)


def interpret(root):
    query_interpreter = QueryInterpreter()
    query_interpreter.visit(root)

    return query_interpreter.expression
