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

# Source code file extensions
exts = ('.c', '.cpp', '.h', '.py', '.rb', '.java')
	
def relpath(directory, filename):
	"""
	Returns a file path that is relative to the given directory
	"""
	filename = filename.replace(directory, '')
	filename = filename[1:] if filename[0] == os.path.sep else filename
	return filename

def get_source_files(repo):
	"""
	Returns a list of the source code files found in the given directory
	"""
	source_files = []
	for root, dirs, files in os.walk(repo):
		for filename in files:
			if os.path.splitext(filename)[1] in exts:
				filename = os.path.join(root, filename)
				source_files.append(relpath(repo, filename))
	return source_files

def build_network(repo):
	"""
	Constructs a bipartite network from the given set of SCM logs
	"""
	source_files = get_source_files(repo)
	logs = parse(repo)
	network = nx.Graph()
	for log in logs:
		network.add_node(log.author, type='author')
		for filename in log.files:
			if filename in source_files:
				network.add_node(filename, type='file')
				network.add_edge(log.author, filename)
	return network


if __name__ == '__main__':
	try:
		import psyco
		psyco.full()
	except ImportError:
		print "Optimization failed. Psyco not found on this machine"
		
	import sys
	if len(sys.argv) < 2:
		sys.exit("Usage: %s [SOURCE_DIR|LOG_FILE]" % sys.argv[0])
	sourcedir = os.path.relpath(sys.argv[1])
	number_of_logs = len(list(parse(sourcedir)))
	network = build_network(sourcedir)
	authors = [n for n in network if network.node[n]['type'] == 'author']
	files = [n for n in network if network.node[n]['type'] == 'file']
	print "Number of Logs:    {0}".format(number_of_logs)
	print "Number of Nodes:   {0}".format(network.number_of_nodes())
	print "Number of Edges:   {0}".format(network.number_of_edges())
	print "Number of Authors: {0}".format(len(authors))
	print "Number of Files:   {0}".format(len(files))
