from qlang_parser import parse_query
from query_interpreter import interpret

import argparse
import utils

queries = {
    'threads': "from threads select id, name, path",
    'average': 'from table select avg(memory)'}

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument(
    '-m',
    '--mode',
    choices=[
        'tree',
        'eval'],
    default='tree',
    nargs='?')
argument_parser.add_argument('-q', '--query', choices=['threads', 'average'])
argument_parser.add_argument('script', action='store', type=str, nargs='?')

arguments = argument_parser.parse_args()

def process_interaction(arguments):
    if arguments.mode == 'tree':
        expression_tree = parse_query(queries[arguments.query])
        utils.display_tree(expression_tree)

        return

    if arguments.mode == 'eval':
        expression_tree = parse_query(queries[arguments.query])

        interpretation_result = interpret(expression_tree)
        print(interpretation_result)


process_interaction(arguments)
