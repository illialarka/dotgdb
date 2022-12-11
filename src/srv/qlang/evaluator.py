import logging

from collections import namedtuple
from lark.visitors import Interpreter 
from source_interpreter import SourceInterpreter 
from select_interpreter import SelectInterpreter

logger = logging.getLogger()

class ExpressionInterpreter(Interpreter):

    def __init__(self, context):
        self._context = context

    def source(self, source_node):
        source_interpreter = SourceInterpreter(self._context)
        source_interpreter.visit(source_node)

    def select_clause(self, select_clause_node):
        select_interpreter = SelectInterpreter(self._context)
        select_interpreter.visit(select_clause_node)

        # code executes after traversing subtree 
        projected_data = []

        for item in self._context.data:
            # TODO: Reqires refactoring
            projected_item = {}
            for field in self._context.projections:
                projected_item[field] = item[field]

            projected_data.append(projected_item)
        self._context.data = projected_data
    
    def condition_expression(self, condition_expression_node):
        print(f'Filtering data set by condition.')

class ExpressionContext:
    '''
    Represents execution context.

    Context contains querying source of data.
    ''' 

    def __init__(self):
        self.data = []
        # list of attr to project
        self.projections = []
    
def evaluate(root):
    expression_context = ExpressionContext()

    expression_tree_visitor = ExpressionInterpreter(expression_context)
    expression_tree_visitor.visit(root)

    return expression_context.data