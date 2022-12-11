from collections import namedtuple
from lark.visitors import Interpreter 

class ExpressionInterpreter(Interpreter):

    def table(self, node):
        print(f'I am in table node: {node}.')

    def condition_expression(self, node):
        print(f'I am in condition expression: {node}.')

    def predicate(self, node):
        print(f'I am in predicate: {node}.')

    def field(self, node):
        print(f'I am in predicate: {node}.')

def evaluate(root):
    expression_tree_visitor = ExpressionInterpreter()
    expression_tree_visitor.visit(root)