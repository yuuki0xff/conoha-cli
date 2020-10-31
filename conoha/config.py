
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
	    1. fromDict引数で指定した値
	    2. 環境変数
	    3. 設定ファイル
	    4. デフォルト値

	configファイルはINI file formatでなければならない。
	環境変数名は"CONOHA_{section}_{key}"で、全て大文字である。
	"""
	endpoint = {
			'account': 'https://account.{REGION}.conoha.io/v1/{TENANT_ID}',
			'compute': 'https://compute.{REGION}.conoha.io/v2/{TENANT_ID}',
			'volume': 'https://block-storage.{REGION}.conoha.io/v2/{TENANT_ID}',
			'database': 'https://database-hosting.{REGION}.conoha.io/v1',
			'image': 'https://image-service.{REGION}.conoha.io/v2',
			'dns': 'https://dns-service.{REGION}.conoha.io/v1',
			'object': 'https://object-storage.{REGION}.conoha.io/v1/nc_{TENANT_ID}',
			'mail': 'https://mail-hosting.{REGION}.conoha.io/v1',
			'identity': 'https://identity.{REGION}.conoha.io/v2.0',
			'network': 'https://networking.{REGION}.conoha.io/v2.0',
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
				'region': 'tyo1',
				},
			}

	def __init__(self, fromFile=None, fromDict=None):
		super().__init__()
		assert(not(fromFile and fromDict))

		self._setDefaultValue()
		if fromFile:
			self.read_file(open(fromFile))
			self._readEnv()
		elif fromDict:
			self._readEnv()
			self.read_dict(fromDict)
		else:
			os.environ.setdefault('XDG_CONFIG_HOME', '~/.config')
			self.read(self._pathExpand_([
				'$XDG_CONFIG_HOME/conoha/config',
				'~/.conoha/conifg',
				]))
			self._readEnv()

		self._translateRegion()

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

	def _translateRegion(self):
		""" endpoint.regionに国名を指定されていた場合、リージョンIDに置き換える。
		これは、後方互換性を維持するための処理。
		"""
		country2region = {
			'japan': 'tyo1',
			'singapore': 'sin1',
			'usa': 'sjc1',
		}
		region = self.get('endpoint', 'region')
		if region in country2region:
			# regionに国名が指定されている。リージョンIDに置き換える。
			self.set('endpoint', 'region', country2region[region])
