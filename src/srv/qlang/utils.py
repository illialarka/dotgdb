from lark import tree
from lark.visitors import CollapseAmbiguities
from matplotlib import pyplot

def display_tree(parsed, file_name='_expression_tree.png'):
   '''
   Displays expressiong tree graph.

   Creates an expression tree image file with name specified by 'file_name'. 
   '''
   expression_trees = CollapseAmbiguities().transform(parsed)

   for expression_tree in expression_trees:
        tree.pydot__tree_to_png(expression_tree, filename=file_name, rankdir='TB')
        pyplot.figure(figsize=(10,10))
        pyplot.imshow(pyplot.imread(file_name))
        pyplot.show()