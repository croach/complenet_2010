#!/usr/bin/env python

from logparser import *
from mercurial import ui, hg
import os

class HgParser(object):
	def __init__(self, source):
		super(HgParser, self).__init__()
		if not os.path.exists(source) or os.path.isfile(source):
			raise IOError("No such repository: '{0}'".format(source))
		self.repo = hg.repository(ui.ui(), source)
		self.logs = self._log_generator(self.repo)
	
	def __iter__(self):
		return self.logs

	def _log_generator(self, repo):
		for i in repo:
			log = repo[i]
			yield Log(
				revision = log.rev(),
				author   = log.user(),
				comment  = log.description(),
				files    = log.files()
			)
