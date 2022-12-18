from lark.visitors import Interpreter


class SelectClauseInterpreter(Interpreter):

    def __init__(self, expression):
        self._expression = expression 

    def field(self, field_node):
        self._expression.projections.append(field_node.children[0].value)
