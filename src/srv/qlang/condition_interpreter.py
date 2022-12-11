from lark.visitors import Interpreter

class ConditionInterpreter(Interpreter):

    def __init__(self, context):
        self._context = context

    def condition_expression(self, condition_expression_node):
        pass
