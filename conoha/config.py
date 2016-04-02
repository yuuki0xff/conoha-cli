
# -*- coding: utf8 -*-
import os
from configparser import SafeConfigParser

__all__ = 'Config'.split()

class Config(SafeConfigParser):
	"""conohaの構成

	引数:
	    fromFile: 構成情報を記録したファイルのパス
	    fromDict: 構成情報のdictオブジェクト

	    fromFile と fromDict は同時に指定できない。
	    fromFile, fromDictどちらも指定しなければ、一番最初に見つかったファイルから構成情報を読み込む
	        ~/.config/conoha/config
	        ~/.conoha/config

	構成情報の優先順位は以下の通り
	    1. 引数により指定された値
	    2. 環境変数
	    3. デフォルト値

	configファイルはINI file formatでなければならない。
	環境変数名は"CONOHA_{section}_{key}"で、全て大文字である。
	"""
	endpoint = {
			'japan': {
				'account': 'https://account.tyo1.conoha.io/v1/{TENANT_ID}',
				'compute': 'https://compute.tyo1.conoha.io/v2/{TENANT_ID}',
				'volume': 'https://block-storage.tyo1.conoha.io/v2/{TENANT_ID}',
				'database': 'https://database-hosting.tyo1.conoha.io/v1',
				'image': 'https://image-service.tyo1.conoha.io/v2',
				'dns': 'https://dns-service.tyo1.conoha.io/v1',
				'object': 'https://object-storage.tyo1.conoha.io/v1/nc_{TENANT_ID}',
				'mail': 'https://mail-hosting.tyo1.conoha.io/v1',
				'identity': 'https://identity.tyo1.conoha.io/v2.0',
				'network': 'https://networking.tyo1.conoha.io/v2.0',
			},
			'singapore': {
				'compute': 'https://compute.sin1.conoha.io/v2/{TENANT_ID}',
				'volume': 'https://block-storage.sin1.conoha.io/v2/{TENANT_ID}',
				'database': 'https://database-hosting.sin1.conoha.io/v1',
				'image': 'https://image-service.sin1.conoha.io/v2',
				'mail': 'https://mail-hosting.sin1.conoha.io/v1',
				'identity': 'https://identity.sin1.conoha.io/v2.0',
				'network': 'https://networking.sin1.conoha.io/v2.0',
			},
			'usa': {
				'compute': 'https://compute.sjc1.conoha.io/v2/{TENANT_ID}',
				'volume': 'https://block-storage.sjc1.conoha.io/v2/{TENANT_ID}',
				'database': 'https://database-hosting.sjc1.conoha.io/v1',
				'image': 'https://image-service.sjc1.conoha.io/v2',
				'mail': 'https://mail-hosting.sjc1.conoha.io/v1',
				'identity': 'https://identity.sjc1.conoha.io/v2.0',
				'network': 'https://networking.sjc1.conoha.io/v2.0',
			},
		}

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
				'region': 'japan',
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
		"""環境変数から設定を読み込む"""
		for key in os.environ:
			if not key.startswith('CONOHA_') or len(key.split('_')) != 3:
				continue

			section = key.split('_')[1].lower()
			if section not in self._defaultValue:
				continue

			parameter = key.split('_')[2].lower()
			if parameter not in self._defaultValue[section]:
				continue

			if section and parameter:
				self[section][parameter] = os.environ[key]

