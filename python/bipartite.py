"""
Functions for creating bipartite graphs from SCM logs

Creates a bipartite graph from SCM logs. The two sets of nodes in the graph
are the authors in the project's community and the files in the repository.
Two nodes are connected if an author has worked on a file according to the 
revision comments in the repository logs.
"""

import networkx as nx
import os

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

def build_network(repo, logs):
	"""
	Constructs a bipartite network from the given set of SCM logs
	"""
	source_files = get_source_files(repo)
	network = nx.Graph()
	for log in logs:
		network.add_node(log.author, type='author')
		for filename in log.files:
			if filename in source_files:
				network.add_node(filename, type='file')
				network.add_edge(log.author, filename)
	return network
