from collections import namedtuple
import os

Log = namedtuple('Log', ('revision', 'author', 'comment', 'files'))	

class LogParser(object):
	def __init__(self, source):
		super(LogParser, self).__init__()
		if not os.path.exists(source):
			raise IOError("No such file or directory: '{0}'".format(source))
		self.source = source
		self.setup()
	
	def __iter__(self):
		return self
					
	def next(self):
		try:
			log = self.parse_log()
		except Exception, e:
			self.cleanup()
			raise StopIteration
		return log

	def setup(self):
		"""
		Opens the IO streams for reading in the logs.
		"""
		if os.path.isdir(self.source):
			self.logs = os.popen("svn log -v {0}".format(self.source))
		else:
			self.logs = open(self.source)
		
	def cleanup(self):
		"""
		Closes all open IO streams.
		"""
		if self.logs:
			self.logs.close()