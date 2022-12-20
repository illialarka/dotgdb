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

    def execute(self, agent):
        if self.source is None:
            print('Source handler has not set.')
            return

        data_set = self.source.handle(agent)
        projected_data = []

        for data_set_item in data_set:
            projected_item = {}

            for projection in self.projections:
                if projection in data_set_item:
                    projected_item[projection] = data_set_item[projection]
                    continue
                else:
                    projected_item[projection] = None

            projected_data.append(projected_item)

        return projected_data