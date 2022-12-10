from lark import Lark
import argparse
import utils 

grammar_path = './grammar.ebnf' 

# Define the ENBF grammar using the Lark parser
enbf_grammar = open(grammar_path).read() 

queries = {
    'plain': "from table where id = 2 and name = divan and name = \"sofa\" or name = \"somevalue\" and id = 3 select field, another, andonemore"
}

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("query", choices=['plain'])

arguments = argument_parser.parse_args() 

# Parse the query using the Lark parser
parser = Lark(grammar=enbf_grammar, start='start', ambiguity='explicit')  
parsed = parser.parse(queries[arguments.query])

utils.display_tree(parsed)