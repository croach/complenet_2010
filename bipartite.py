#!/usr/bin/env python

"""
Creates a bipartite graph from SCM logs

Creates a bipartite graph from SCM logs. The two sets of nodes in the graph
are the authors in the project's community and the files in the repository.
Two nodes are connected if an author has worked on a file according to the 
revision comments in the repository logs.
"""

import networkx as nx
import os

from logparser import parse

SOURCE_CODE_EXTENSIONS = ['.c', '.cpp', '.h', '.py', '.rb', '.java']

def build_network(logs):
	"""
	Constructs a bipartite network from the given set of SCM logs
	"""
	network = nx.Graph()
	for log in logs:
		network.add_node(log.author, type='author')
		for filename in log.files:
			if os.path.splitext(filename)[1] in SOURCE_CODE_EXTENSIONS:
				network.add_node(filename, type='file')
				network.add_edge(log.author, filename)
	return network


if __name__ == '__main__':
	import sys
	if len(sys.argv) < 3:
		print ("Usage: %s [SOURCE_DIR|LOG_FILE] [svn|git|hg]" %
			sys.argv[0])
		sys.exit()
	number_of_logs = len(list(parse(sys.argv[1], sys.argv[2])))
	logs = parse(sys.argv[1], sys.argv[2])
	network = build_network(logs)
	authors = [n for n in network if network.node[n]['type'] == 'author']
	files = [n for n in network if network.node[n]['type'] == 'file']
	print "Number of Logs:    {0}".format(number_of_logs)
	print "Number of Nodes:   {0}".format(network.number_of_nodes())
	print "Number of Edges:   {0}".format(network.number_of_edges())
	print "Number of Authors: {0}".format(len(authors))
	print "Number of Files:   {0}".format(len(files))
