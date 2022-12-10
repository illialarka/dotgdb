from lark import Lark
import utils 

grammar_path = './grammar.lark' 

# Define the ENBF grammar using the Lark parser
enbf_grammar = open(grammar_path).read() 

# Parse the query using the Lark parser
query = "from table where id = 2 and name = divan and name = \"sofa\" select field"

parser = Lark(grammar=enbf_grammar, start='start', ambiguity='explicit')  
parsed = parser.parse(query)

utils.display_tree(parsed)