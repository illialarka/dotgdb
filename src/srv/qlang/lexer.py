from lark import Lark
from lark.tree import Tree
from graphviz import Digraph

grammar = r"""
%import common.NUMBER
%import common.WS

fields: "id" | "name"

!expr : expr fields expr

query: "select"

from: "from"

%ignore WS
"""

def parse_tree_to_graph(tree: Tree, graph: Digraph):
    for child in tree.children:
        if isinstance(child, Tree):
            parse_tree_to_graph(child, graph)
        else:
            graph.node(child.value, label=child.value)
            graph.edge(tree.data, child.value)

def generate_graph(parser: Lark, input_string: str):
    tree = parser.parse(input_string)

    graph = Digraph()
    parse_tree_to_graph(tree, graph)

    return graph

parser = Lark(grammar=grammar, start='expr', ambiguity='explicit')  
input_string = "select fields from"

graph = generate_graph(parser, input_string)

# You can save the graph to a file using the following code:
graph.render('graph.gv', view=True)
