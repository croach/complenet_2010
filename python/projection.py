"""
Functions for creating one-mode projections of bipartite graphs
"""

import networkx as nx
from utilities import *
	
def project_graph(g, nodes):
	"""
	Projects the bipartite graph 'g' onto the given set of nodes
	"""
	projection = nx.Graph()
	for n in nodes:
		edges = combine(g[n].keys())
		for e in edges:
			if projection.has_edge(*e):
				# Increment the edge weight
				projection[e[0]][e[1]]['weight'] += 1
			else:
				# Add the new edge to the projected graph
				projection.add_edge(e[0], e[1], {'weight':1})
	return projection


