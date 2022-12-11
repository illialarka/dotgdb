from qlang_parser import parse_query
from evaluator import evaluate 
import argparse
import utils 

queries = {
    'plain': "from table where id = 2 and name = divan and name = \"sofa\" or name = \"somevalue\" and id = 3 select field, another, andonemore",
    'average': 'from table select avg(memory)'
}

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('mode', choices=['tree', 'eval'], default='tree', nargs='?')
argument_parser.add_argument('--query', choices=['plain', 'average'])

arguments = argument_parser.parse_args() 

print(arguments)

def process_interaction(arguments):
    if arguments.mode == 'tree':
        expression_tree = parse_query(queries[arguments.query]) 
        utils.display_tree(expression_tree)

        return
    
    if arguments.mode == 'eval':
        expression_tree = parse_query(queries[arguments.query]) 
        # IDK what is going on, YET
        evaluate(expression_tree)

process_interaction(arguments)