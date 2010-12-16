#!/usr/bin/env python

"""
Functions for performing a series of tests on a repository's networks
"""

try:
	import psyco
	psyco.full()
except ImportError:
	print "Optimization failed. Psyco not found on this machine"	
import sys
import random

from logparser import parse
from bipartite import *
from projection import *
from decomp import *
from authors import redundant_authors

def sort_dict(dictionary, descending=False):
	"""
	Given a dict, returns a list of keys sorted by the values
	
	Parameters:
	  dictionary - dictionary object to sort
	  descending - if true, sort descending
	"""
	results = [(value, key) for key, value in dictionary.iteritems()]
	results = sorted(results, reverse=descending)
	results = [key for value, key in results]
	return results
	
def decomp_by_random(g1, g2, nodes):
	nodes_random_order = random.sample(nodes, len(nodes))
	results = decompose(g1, g2.copy(), nodes_random_order)
	return results

def decomp_by_commit_count(g1, g2, logs):
	commits = {}
	for log in logs:
		if log.author not in commits:
			commits[log.author] = 0
		commits[log.author] += 1
	nodes_by_commits = sort_dict(commits, descending=True)
	results = decompose(g1, g2.copy(), nodes_by_commits)
	return results
	
def decomp_by_degree(g1, g2, nodes):
	degrees = nx.degree(g1, nodes)
	nodes_by_degree = sort_dict(degrees, descending=True)
	results = decompose(g1, g2.copy(), nodes_by_degree)
	return results
	
def decomp_by_closeness(g1, g2, nodes):
	closeness = dict(
		[(node, nx.closeness_centrality(g1, node)) for node in nodes])
	nodes_by_closeness = sort_dict(closeness, descending=True)
	results = decompose(g1, g2.copy(), nodes_by_closeness)
	return results

def decomp_by_betweenness(g1, g2, nodes):
	betweenness = nx.betweenness_centrality(g1)
	betweenness = dict([(node, betweenness[node]) for node in nodes])
	nodes_by_betweenness = sort_dict(betweenness, descending=True)
	results = decompose(g1, g2.copy(), nodes_by_betweenness)
	return results

def print_results(results):
	sys.stdout.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(
		'Random',
		'Commit Count',
		'Degree',
		'Closeness',
		'Betweenness'))
	for i in xrange(len(results['random'])):
		sys.stdout.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(
			results['random'][i],
			results['commits'][i],
			results['degree'][i],
			results['closeness'][i],
			results['betweenness'][i]
		))

def remove_redundant_authors(logs):
	"""
	Replaces all author names in the logs with the matching author name
	found in the redundant authors dict.
	"""
	return [log._replace(author=redundant_authors.get(log.author, log.author)) 
			for log in logs]

def main():
	if len(sys.argv) < 2:
		sys.exit("Usage: %s [SOURCE_DIR|LOG_FILE]" % sys.argv[0])
	sourcedir = os.path.relpath(sys.argv[1])
	logs = list(parse(sourcedir))
	remove_redundant_authors(logs)
	network = build_network(sourcedir, logs)
	authors = [n for n in network if network.node[n]['type'] == 'author']
	projection = project_graph(network, authors)
	
	results = {
		'random'      : decomp_by_random(network, projection, authors),
		'commits'     : decomp_by_commit_count(network, projection, logs),
		'degree'      : decomp_by_degree(network, projection, authors),
		'closeness'   : decomp_by_closeness(network, projection, authors),
		'betweenness' : decomp_by_betweenness(network, projection, authors)
	}
	print_results(results)


if __name__ == '__main__':
	main()