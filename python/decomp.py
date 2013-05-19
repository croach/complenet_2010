"""
Functions for decomposing a graph 
"""

import networkx as nx
from utilities import *

def largest_component_size(g):
	"""
	Calculates the size of the largest component in the graph g
	"""
	components = nx.connected_components(g)
	return max([len(c) for c in components])

def remove_edges(g, edges):
	"""
	Decrements the weight of each edge in the edges list and removes any 
	edge whose weight is zero or below.
	"""
	# Decrement and remove all edges associated with the node being removed
	for e in edges:
		if g.has_edge(*e):
			g[e[0]][e[1]]['weight'] -= 1
			if g[e[0]][e[1]]['weight'] <= 0:
				g.remove_edge(*e)

def decompose(g1, g2, nodes):
	"""
	Decomposes a graph according to a list of nodes and returns a list
	containing the size of the largest component in the graph at each
	stage of the decomposition.
	
	The nodes parameter is a list of nodes in the graph g1. These nodes are 
	represented by edge weights in the one-mode projection g2. As each node
	is removed the weight of edges correpsonding to the node is decremented 
	in g2 until the weight reaches zero at which time the edge is removed 
	from the graph completely.
	
	Parameters:
	  g1      - The original bipartite graph
	  g2      - The one-mode projection of g1
	  nodes   - The nodes to be removed from the graph
	"""
	results = [largest_component_size(g2)]
	for n in nodes:
		edges = combine(g1.edge[n].keys())
		remove_edges(g2, edges)
		results.append(largest_component_size(g2))
	return results
