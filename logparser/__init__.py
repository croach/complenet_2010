from svnparser import SvnParser
from gitparser import GitParser
from hgparser import HgParser

def parse(source, type):
	if type == "svn":
		return SvnParser(source)
	elif type == "git":
		return GitParser(source)
	elif type == "hg":
		return HgParser(source)
	else:
		raise ValueError("Type '{0}' does not exist".format(type))
		
__all__ = ["parse"]
		