import exceptions

from lark.visitors import Interpreter

class SourceInterpreter(Interpreter):
    '''
    An example of a source subtree.

            [source]
            /
        table
        /
    Token (WORD, <source>)

    or

            [source]
            /
        subquery 
        /
      TBD

    The result of the execution is a query date set from the source.
    '''

    def __init__(self, context):
        self._context = context

    def table(self, table_node):
        '''
        Evaluates subtree:

            table
            /
        Token (WORD, <source>)
        '''

        if len(table_node.children) != 1:
            raise exceptions.IncorrectChildNumerError

        source_token = table_node.children[0]

        self._context.data = [
            {
                'id': 1,
                'name': 'sofa'
            },
            {
                'id': 2,
                'name': 'chair'
            },
            {
                'id': 3,
                'name': 'bed'
            }]

        print(f'Requesting data from table: "{source_token.value}".')