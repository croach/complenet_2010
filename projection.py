import networkx as nx

	
def combine(lst):
	"""
	Creates a list of combinations of the items in the given list
	"""
	return [(lst[i], lst[j]) 
			for i in xrange(len(lst)) 
			for j in xrange(i+1,len(lst))]
	
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


