"""
A collection of common utility functions
"""

def combine(lst):
	"""
	Creates a list of combinations of the items in the given list
	"""
	return [(lst[i], lst[j]) 
			for i in xrange(len(lst)) 
			for j in xrange(i+1,len(lst))]
	
