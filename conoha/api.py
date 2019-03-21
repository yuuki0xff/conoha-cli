
# -*- coding: utf8 -*-
from urllib.request import Request, urlopen
import json

__all__ = 'API'.split()

class DictWrapper(dict):
	""" dictインスタンスへインスタンス変数を追加するために使用する """
	pass
class BytesWrapper(bytes):
	""" bytesインスタンスへインスタンス変数を追加するために使用する """
	pass

class API:
	"""全てのConoHa APIを呼び出すクラスのスーパークラス"""
	def __init__(self, token=None, baseURIPrefix=None):
		self.__baseURI = None
		self.token = token
		self._serviceType = None
		self.baseURIPrefix = baseURIPrefix

	def _getHeaders(self, h):
		headers={
				'Accept': 'application/json',
				}
		if self.token:
			headers['X-Auth-Token'] = self.token.getAuthToken()
		if h:
			headers.update(h)
		return headers

	def _GET(self, path, data=None, isDeserialize=True, headers=None, method='GET'):
		"""APIを呼び出す

		dataにNone以外を指定した場合は、jsonに変換してアップロードする
		headersにはdictを指定した場合は、リクエストに指定したヘッダーを追加する

		レスポンスは、DictWrapperオブジェクトかBytesWrapperオブジェクト
		レスポンスには、下記の属性を含む
		    code:int      http status code
			msg:str       http status message
			headers:dict  レスポンスヘッダー
		"""
		# set self.__baseURI
		if not self.__baseURI:
			if self.token:
				self.__baseURI = self.token.getEndpointURL(self._serviceType)
			else:
				self.__baseURI = self.getEndpointURL(self._serviceType)

			if self.baseURIPrefix:
				self.__baseURI += '/' + self.baseURIPrefix

		if data:
			data = bytes(json.dumps(data), 'utf8')
		req = Request(
				url=self.__baseURI + ('/' + path if path else ''),   # 末尾の'/'はつけない
				headers=self._getHeaders(headers),
				method=method,
				data=data,
				)
		with urlopen(req) as res:
			resBin = res.read()
			if isDeserialize:
				data = DictWrapper(json.loads(str(resBin, 'utf8')))
			else:
				data = BytesWrapper(resBin)
			# HTTPステータスコードとヘッダーを追加
			data.code = res.code
			data.msg = res.msg
			data.headers = res.headers
			return data

	def _DELETE(self, *args, **nargs):
		"""see help(self._GET)"""
		return self._GET(*args, method='DELETE', **nargs)

	def _POST(self, path, data, *args, **nargs):
		"""see help(self._GET)"""
		return self._GET(path, data, *args, method='POST', **nargs)

	def _PUT(self, path, data, *args, **nargs):
		"""see help(self._GET)"""
		return self._GET(path, data, *args, method='PUT', **nargs)

class Token(API):
	def __init__(self, conf):
		super().__init__()
		self._serviceType = 'identity'
		self.conf = conf
		path = 'tokens'
		data = { 'auth':{
			'passwordCredentials':{
				'username': conf.get('api', 'user'),
				'password': conf.get('api', 'passwd'),
				},
			}}
		self.tenantId = conf.get('api', 'tenant')
		if self.tenantId:
			data['auth']['passwordCredentials']['tenantId'] = self.tenantId
		res = self._POST(path, data)
		self.token = res['access']['token']

	def getTenantId(self):
		return self.tenantId
	def getAuthToken(self):
		return self.token['id']
	def getEndpointURL(self, name):
		url = self.conf.get('endpoint', name, fallback=None) or self.conf.endpoint[self.conf.get('endpoint', 'region')][name]
		assert(url)
		if '{TENANT_ID}' in url:
			url = url.replace('{TENANT_ID}', self.getTenantId())
		return url.rstrip('/')

class CustomList(list):
	"""インデックス指定の拡張を支援する
	インデックスが int または slice で指定された場合は、通常のリスト同様の動作をする
	それ以外のオブジェクトを指定した場合は、_getitemメソッドが最初にTrueを返したitemを返す

	サブクラスは_getitem(key, item)メソッドを実装しなければならない
	"""
	def __getitem__(self, key):
		if isinstance(key, int) or isinstance(key, slice):
			return super().__getitem__(key)
		else:
			for item in self:
				if self._getitem(key, item):
					return item
			raise KeyError(key)

