from lark import Lark, Transformer, tree
import matplotlib.pyplot as plt
from lark.visitors import CollapseAmbiguities
from pathlib import Path

grammar_path = './grammar.lark' 

# Define the ENBF grammar using the Lark parser
enbf_grammar = open(grammar_path).read() 

# Create the Lark parser using the ENBF grammar
enbf_parser = Lark(enbf_grammar)


# Define the query transformer to convert the parse tree into a more useful format
class QueryTransformer(Transformer):
    def query(self, items):
        return {
            "projections": items[0],
            "sources": items[1],
            "condition": items[2]
        }

    def projection(self, items):
        if len(items) == 1:
            return items[0]
        else:
            return {
                "field": items[0],
                "alias": items[2]
            }

    def field(self, items):
        return items[0]

    def source(self, items):
        return items[0]

    def subquery(self, items):
        return items[1]

    def condition(self, items):
        print(f'I am at condition: {items}')
        if len(items) == 3:
            return {
                "field": items[0],
                "operator": items[1],
                "value": items[2]
            }

        return {
            "value": items[0]
        }

    def operator(self, items):
        print(f'I am at operator: {items}')

    def expression(self, items):
        return {
            "function": items[0],
            "expressions": items[1]
        }

    def function(self, items):
        return items[0]

    def expressions(self, items):
        return items


# Create the query transformer
query_transformer = QueryTransformer()

# Parse the query using the Lark parser
query = "FROM table WHERE id = 2 and name = \"divan\" select field"
parse_tree = enbf_parser.parse(query)

# Transform the parse tree into a more useful format
transformed_query = query_transformer.transform(parse_tree)

# Print the transformed query
print(transformed_query)

def plot_trees(grammar:str, text:str, start='query'):
    parser = Lark(grammar=grammar, start=start, ambiguity='explicit')  
    parsed = parser.parse(text)
    trees = CollapseAmbiguities().transform(parsed)
    for t in trees:
        tree.pydot__tree_to_png(t, filename='tree.png', rankdir='TB')
        plt.figure(figsize=(10,10))
        plt.imshow(plt.imread("tree.png"))
        plt.show()

plot_trees(enbf_grammar, query)
