from lark import tree
from lark.visitors import CollapseAmbiguities
from matplotlib import pyplot

def display_tree(parsed_expression_tree, file_name='_expression_tree.png'):
   for expression_tree in CollapseAmbiguities().transform(parsed_expression_tree):
      tree.pydot__tree_to_png(expression_tree, filename=file_name, rankdir='TB')
      pyplot.figure(figsize=(10,10))
      pyplot.imshow(pyplot.imread(file_name))
      pyplot.show()