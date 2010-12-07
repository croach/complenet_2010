#!/usr/bin/env python

from log import Log
import os
import re

REDUNDANT_AUTHORS = {
    'aimacintyre'    : 'andrew.macintyre',
    'akuchlin'       : 'andrew.kuchling',
    'akuchling'      : 'andrew.kuchling',
    'andrewmcnamara' : 'andrew.mcnamara',
    'anthonybaxter'  : 'anthony.baxter',
    'arigo'          : 'armin.rigo',
    'guido'          : 'guido.van.rossum',
    'gvanrossum'     : 'guido.van.rossum',
    'gward'          : 'greg.ward',
    'jackjansen'     : 'jack.jansen',
    'loewis'         : 'martin.v.loewis',
    'mhammond'       : 'mark.hammond',
    'nnorwitz'       : 'neal.norwitz',
    'niemeyer'       : 'gustavo.niemeyer',
    'rhettinger'     : 'raymond.hettinger',
    'sjoerd'         : 'sjoerd.mullender',
    'theller'        : 'thomas.heller',
    'tim_one'        : 'tim.peters'
}

log_re = re.compile(r'^r(\d+) \| ([^ |]+) \| [^|]+ \| (\d+) lines?')
file_re = re.compile(r'^\s+[A-Z] (.+)')

LOG_DELIM = '-'*72

class SvnParser(object):
	def __init__(self, source):
		super(SvnParser, self).__init__()
		if not os.path.exists(source):
			raise IOError("No such file or directory: '{0}'".format(source))
		self.source = source
		self.setup()
	
	def __iter__(self):
		return self
					
	def next(self):
		try:
			log = None
			while not log:
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
			
	def next_log(self):
		"""
		Parses the next log in the stream and returns a list of its lines.
		"""
		log = []
		while True:
			line = next(self.logs)
			if line.rstrip() == LOG_DELIM:
				break
			log.append(line)
		return log
		
	def parse_log(self):
		"""
		Parses the next log in the stream and returns a Log object 
		representing it.
		"""
		string = ''.join(self.next_log()).strip()
		m = log_re.match(string)
		if m:	
			log = Log(
				revision = m.groups()[0],
				author   = REDUNDANT_AUTHORS.get(m.groups()[1], m.groups()[1]),
				comment  = self.parse_comment(string, int(m.groups()[2])),
				files    = self.parse_files(string))
			return log
		return None

	def parse_comment(self, string, length):
		"""
		Parses the comment in the current log.
		"""
		lines = string.split('\n')
		for i in range(len(lines)):
			if not lines[i].strip():
				return '\n'.join(lines[i+1:i+10])
		return None

	def parse_files(self, string):
		"""
		Parses the list of files changed files for the current log.
		"""
		files = []
		parsing_on = False
		for line in string.split('\n'):
			if line.strip() == 'Changed paths:':
				parsing_on = True
			if parsing_on:
				if not line.strip():
					break
				m = file_re.match(line) 
				if m:
					filepath = self.remove_root(m.groups()[0])
					files.append(filepath)
		return files

	def remove_root(self, filepath):
		"""
		Removes the root directory from the given path
		
		SVN adds '/repo/' to the begining of all filepaths. This function
		removes that prefix to make the filepath relative to the repo.
		"""
		path_components = filepath.split(os.path.sep)
		path_components = path_components[2:] # Remove the root directory
		return os.path.sep.join(path_components)
