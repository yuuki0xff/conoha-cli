
# -*- coding: utf8 -*-
import os
from configparser import SafeConfigParser

__ALL__ = 'Config'.split()

class Config(SafeConfigParser):
	_defaultValue = {
			'api': {
				'user': '',
				'passwd': '',
				'tenant': '',

				'timeout': 30,
				'retry': 0,
				},
			'compute': {
				'soft_limit': -1,
				'hard_limit': -1,
				'allow_plans': '',
				},
			}

	def __init__(self):
		super().__init__()
		self._setDefaultValue()
		self._readEnv()
		os.environ.setdefault('XDG_CONFIG_HOME', '~/.config')
		self.read(self._pathExpand_([
			'$XDG_CONFIG_HOME/conoha/config',
			'~/.conoha/conifg',
			]))

	def _pathExpand_(self, pathList):
		for i, item in enumerate(pathList):
			pathList[i] = os.path.expanduser(os.path.expandvars(item))
		return pathList

	def _setDefaultValue(self):
		self.read_dict(self._defaultValue)

	def _readEnv(self):
		for key in os.environ:
			if not key.startswith('CONOHA_') or len(key.split('_')) != 3:
				continue

			section = key.split('_')[1].upper()
			if section.lower() not in self._defaultValue:
				continue

			parameter = key.split('_')[2].upper()
			if parameter.lower() not in self._defaultValue[section]:
				continue

			if section and parameter:
				self[section][parameter] = os.environ[key]

