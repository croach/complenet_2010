#!/usr/bin/env python

from logparser import *
from git import *
import os

class GitParser(object):
	def __init__(self, source):
		super(GitParser, self).__init__()
		if not os.path.exists(source) or os.path.isfile(source):
			raise IOError("No such repository: '{0}'".format(source))
		self.repo = Repo(source)
		self.logs = self._log_generator(self.repo)
	
	def __iter__(self):
		return self.logs

	def _log_generator(self, repo):
		for log in repo.iter_commits():
			yield Log(
				revision = log.hexsha,
				author   = log.committer,
				comment  = log.message,
				files    = self._files(log)
			)
			
	def _files(self, log):
		g = self.repo.git
		result = g.show(log.hexsha, pretty="format:", name_only=True)
		return result.strip().split('\n')
		
