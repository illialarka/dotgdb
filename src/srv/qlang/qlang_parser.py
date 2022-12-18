from lark import Lark
import os

module_path = os.path.dirname(os.path.realpath(__file__))
grammar_path = os.path.join(module_path, 'grammar.lark')

# Import EBNF grammar
enbf_grammar = open(grammar_path).read() 

parser = Lark(grammar=enbf_grammar, start='start', ambiguity='explicit')  

def parse_query(query):
    return parser.parse(query)