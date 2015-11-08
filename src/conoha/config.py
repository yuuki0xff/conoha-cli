
# -*- coding: utf8 -*-
import os
from configparser import SafeConfigParser

__ALL__ = 'Config'.split()

class Config(SafeConfigParser):
	def __init__(self):
		super().__init__()
		os.environ.setdefault('XDG_CONFIG_HOME', '~/.config')
		self.read(self._pathExpand_([
			'$XDG_CONFIG_HOME/conoha/config'
			'~/.conoha/conifg',
			]))

	def _pathExpand_(self, pathList):
		for i, item in enumerate(pathList):
			pathList[i] = os.path.expanduser(os.path.expandvars(item))
		return pathList

