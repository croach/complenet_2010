from svnparser import SvnParser

def parse(source, type):
	if type == "svn":
		return SvnParser(source)
		
__all__ = ["parse"]
		