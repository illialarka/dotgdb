from lark import Lark

# Import EBNF grammar
grammar_path = './grammar.lark' 
enbf_grammar = open(grammar_path).read() 

parser = Lark(grammar=enbf_grammar, start='start', ambiguity='explicit')  

def parse_query(query):
    return parser.parse(query)