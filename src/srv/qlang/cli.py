import argparse
import utils 
from qlang_parser import parse_query

queries = {
    'plain': "from table where id = 2 and name = divan and name = \"sofa\" or name = \"somevalue\" and id = 3 select field, another, andonemore",
    'average': 'from table select avg(memory)'
}

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("query", choices=['plain', 'average'])

arguments = argument_parser.parse_args() 

expression_tree = parse_query(queries[arguments.query]) 
utils.display_tree(expression_tree)