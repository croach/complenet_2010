#!/usr/bin/env python

try:
	import psyco
	psyco.full()
except ImportError:
	print "Optimization failed. Psyco not found on this machine"	
import sys

from logparser import parse
from bipartite import *
from projection import *

def main():
	"""
	Creates a bipartite network from the given source directory and then 
	projects it onto the list of file nodes.
	"""
	if len(sys.argv) < 2:
		sys.exit("Usage: %s [SOURCE_DIR|LOG_FILE]" % sys.argv[0])
	sourcedir = os.path.relpath(sys.argv[1])
	logs = list(parse(sourcedir))
	network = build_network(sourcedir, logs)
	authors = [n for n in network if network.node[n]['type'] == 'author']
	files = [n for n in network if network.node[n]['type'] == 'file']
	print "Number of Logs:    {0}".format(len(logs))
	print "Number of Nodes:   {0}".format(network.number_of_nodes())
	print "Number of Edges:   {0}".format(network.number_of_edges())
	print "Number of Authors: {0}".format(len(authors))
	print "Number of Files:   {0}".format(len(files))
	
	projection = project_graph(network, authors)
	print "Number of Nodes:   {0}".format(projection.number_of_nodes())
	print "Number of Edges:   {0}".format(projection.number_of_edges())
	print "Number of Files:   {0}".format(len(files))
	
	
if __name__ == '__main__':
	main()