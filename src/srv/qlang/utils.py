from lark import tree
from lark.visitors import CollapseAmbiguities
import matplotlib.pyplot as plt

def display_tree(parsed):
   trees = CollapseAmbiguities().transform(parsed)
   for t in trees:
        tree.pydot__tree_to_png(t, filename='tree.png', rankdir='TB')
        plt.figure(figsize=(10,10))
        plt.imshow(plt.imread("tree.png"))
        plt.show()
