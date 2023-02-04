import logging

logger = logging.getLogger()


class QueryExpression:
    '''
    Represents QLang query in a comipled expression.

    A query expression does not require parse and traverse
    token tree, it is already parsed and traversed. 

    A query can be queried many times.  

    The purpose of the type is to provide intermediate
    representation of a query to make query manipulation/storing.
    '''

    def __init__(self):
        self.source = None 
        self.projections = set() 
        self.query = None

    def execute(self, agent, event):
        if self.source is None:
            logger.info('Source handler has not been set.')
            return

        data_items = self.source.handle(agent, event)
        projected_data = []

        for data_item in data_items:
            projected_item = dict() 

            for projection in self.projections:
                projected_item[projection] = getattr(data_item, projection) 

            projected_data.append(projected_item)

        return projected_data
