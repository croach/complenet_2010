#!/usr/bin/env python

from logparser import *
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

class SvnParser(LogParser):
	def __init__(self, source):
		super(SvnParser, self).__init__(source)
			
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
		# If log is blank, return the next log
		if log:
			return log
		else:
			return self.next_log() 
		
	def parse_log(self):
		"""
		Parses the next log in the stream and returns a Log object 
		representing it.
		"""
		string = ''.join(self.next_log())
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
					files.append(m.groups()[0])
		return files
