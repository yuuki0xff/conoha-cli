
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
			'endpoint': {
				# url of endpoint in Tokyo.
				'account': 'https://account.tyo1.conoha.io/v1/{TENANT_ID}',
				'compute': 'https://compute.tyo1.conoha.io/v2/{TENANT_ID}',
				'volume': 'https://block-storage.tyo1.conoha.io/v2/{TENANT_ID}',
				'database': 'https://database-hosting.tyo1.conoha.io/v1',
				'image': 'https://image-service.tyo1.conoha.io',
				'dns': 'https://dns-service.tyo1.conoha.io',
				'object': 'https://object-storage.tyo1.conoha.io/v1/nc_{TENANT_ID}',
				'mail': 'https://mail-hosting.tyo1.conoha.io/v1',
				'identity': 'https://identity.tyo1.conoha.io/v2.0',
				'network': 'https://networking.tyo1.conoha.io',
				},
			}

	def __init__(self, fromFile=None, fromDict=None):
		super().__init__()
		assert(not(fromFile and fromDict))

		self._setDefaultValue()
		self._readEnv()
		if fromFile:
			self.read_file(open(fromFile))
		elif fromDict:
			self.read_dict(fromDict)
		else:
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

