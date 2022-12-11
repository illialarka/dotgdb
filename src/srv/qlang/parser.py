from lark import Lark
import argparse
import utils 

grammar_path = './grammar.lark' 

enbf_grammar = open(grammar_path).read() 

queries = {
    'plain': "from table where id = 2 and name = divan and name = \"sofa\" or name = \"somevalue\" and id = 3 select field, another, andonemore",
    'average': 'from table select avg(memory)'
}

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("query", choices=['plain', 'average'])

arguments = argument_parser.parse_args() 

parser = Lark(grammar=enbf_grammar, start='start', ambiguity='explicit')  
parsed = parser.parse(queries[arguments.query])

utils.display_tree(parsed)