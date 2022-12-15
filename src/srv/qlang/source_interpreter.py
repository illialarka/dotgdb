from exceptions import InvalidSourceNameException
from lark.visitors import Interpreter
from threads_source_token_handler import ThreadsSourceTokenHandler

source_token_handlers = [
    ThreadsSourceTokenHandler()
]


class SourceClauseInterpreter(Interpreter):

    def __init__(self, agent, context):
        self._agent = agent
        self._context = context

    def table(self, table_node):
        table_name_token = table_node.children[0]
        table_name_token_handler = self._find_table_token_handler(
            table_name_token.data)

        if table_name_token_handler is None:
            raise InvalidSourceNameException

        self._context.data = table_name_token_handler.handle(self._agent)

    def _find_table_token_handler(self, source):
        for token_handler in source_token_handlers:
            if token_handler.can_handle(source):
                return token_handler
        return None
