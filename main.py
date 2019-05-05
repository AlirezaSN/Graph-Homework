################### imports ###################

import networkx as nx
import matplotlib.pyplot as plt

################### code ###################

g = nx.read_edgelist('datasets/facebook_combined.txt', create_using=nx.Graph(), nodetype=int)
print(nx.info(g))