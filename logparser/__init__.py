from svnparser import SvnParser
from gitparser import GitParser
from hgparser import HgParser

import os

def parse_repo(source):
	"""
	Determines the type of repository (svn, git, or hg) that source references
	"""
	isrepo = lambda repo_dir: os.path.exists(os.path.join(source, repo_dir))
	if not os.path.exists(source):
		repo = None
	elif os.path.isdir(source):
		if isrepo('.git'):
			repo = "git"
		elif isrepo('.svn'):
			repo = "svn"
		elif isrepo('.hg'):
			repo = "hg"
		else:
			repo = None
	elif os.path.isfile(source):
		repo = os.path.splitext(source)[1][1:]
	else:
		repo = None
	return repo
	
def parse(source):
	repo = parse_repo(source)
	if repo == "svn":
		return SvnParser(source)
	elif repo == "git":
		return GitParser(source)
	elif repo == "hg":
		return HgParser(source)
	else:
		raise ValueError("{0} is not of type svn, git, or hg".format(type))
		
	
__all__ = ["parse"]
		