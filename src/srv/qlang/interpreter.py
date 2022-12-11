import logging

from lark.visitors import Interpreter 
from source_interpreter import SourceInterpreter 
from select_interpreter import SelectInterpreter

logger = logging.getLogger()

class ExpressionInterpreter(Interpreter):
    '''
    Interprets QLang query and performs query actions.

    Context requires single place where information stored during 
    expression tree traversing (including data set).
    '''

    def __init__(self, context):
        self._context = context

    def source(self, source_node):
        source_interpreter = SourceInterpreter(self._context)
        source_interpreter.visit(source_node)

        # techically there should be logic
        # getting data accoring to entity we query

    def select_clause(self, select_clause_node):
        select_interpreter = SelectInterpreter(self._context)
        select_interpreter.visit(select_clause_node)

        # code executes after traversing subtree 
        projected_data = []

        for data_item in self._context.data:
            projected_item = {}

            for field_name in self._context.projections:
                # print(f'test {field_name}, has {field_name in data_item}, data: {data_item}')
                if field_name in data_item: 
                    projected_item[field_name] = data_item[field_name]
                    continue
                else:
                    projected_item[field_name] = None

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
    
def interpret(root):
    expression_context = ExpressionContext()

    expression_tree_visitor = ExpressionInterpreter(expression_context)
    expression_tree_visitor.visit(root)

    return expression_context.data