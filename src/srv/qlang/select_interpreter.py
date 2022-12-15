from lark.visitors import Interpreter


class SelectClauseInterpreter(Interpreter):

    def __init__(self, context):
        self._context = context

    def field(self, field_node):
        self._context.projections.append(field_node.children[0].value)
