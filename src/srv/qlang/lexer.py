from graphviz import Digraph
from lark.visitors import CollapseAmbiguities
import matplotlib.pyplot as plt
from lark import Lark, tree, Tree

# Define the ENBF grammar for SQL
grammar = """
%import common.ESCAPED_STRING
%import common.INT
%import common.WORD
%import common.WS
%ignore WS

!query       : [SELECT] projection [FROM source] [WHERE condition] [ORDER BY ordering] [LIMIT integer]
projection  : [DISTINCT] item [item]*
item        : WORD | INT | function
function    : identifier "(" [parameters] ")"
parameters  : parameter [parameter]*
parameter   : item | constant
source      : identifier [identifier]*
condition   : expression [AND|OR expression]*
expression  : item operator constant | "(" condition ")"
ordering    : identifier [ASC|DESC] [identifier [ASC|DESC]]*
identifier  : integer 
operator    : "=" | "<" | ">" | "<=" | ">=" | "<>"
integer     : INT 
constant    : ESCAPED_STRING

SELECT: "SELECT"
DISTINCT: "DISTINCT"
FROM: "FROM"
WHERE: "WHERE"
GROUP: "GROUP"
BY: "BY"
ORDER: "ORDER"
ASC: "ASC"
DESC: "DESC"
LIMIT: "LIMIT"
AND: "AND"
OR: "OR"
"""

# Create a parser using the defined grammar
parser = Lark(grammar, start='query')

input_str = """
SELECT name FROM users WHERE age = "abc"
"""

def parse_tree_to_graph(tree: Tree, graph: Digraph):
    if tree is  None:
        return

    for child in tree.children:
        if child is None:
            continue
        if isinstance(child, Tree):
            parse_tree_to_graph(child, graph)
        else:
            graph.node(child.value, label=child.value)
            graph.edge(tree.data, child.value)

def generate_graph(parser: Lark, input_string: str):
    tree = parser.parse(input_string)
    print(tree)

    graph = Digraph()
    parse_tree_to_graph(tree, graph)

    return graph


#graph = generate_graph(parser, input_str)

#graph.render('graph.gv', view=True)



def plot_trees(grammar:str,  text:str, start='query'):
    parser = Lark(grammar=grammar, start=start,ambiguity='explicit')  
    parsed = parser.parse(text)
    tree.pydot__tree_to_png(parsed, filename='tree.png', rankdir='TB')
    plt.figure(figsize=(18,18))
    plt.imshow(plt.imread("tree.png"))
    plt.show()

plot_trees(grammar, input_str)