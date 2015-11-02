
# -*- coding: utf8 -*-
from urllib.request import Request, urlopen
import json
__ALL__ = 'API Tenant'.split()

class API:
	baseURI = 'https://identity.tyo1.conoha.io'
	identity = None

	def _getHeaders(self, h):
		headers={
				'Accept': 'application/json',
				}
		if self.identity:
			headers['X-Auth-Token'] = self.identity.getAuthToken()
		if h:
			headers.update(h)
		return headers

	def _GET(self, path, data=None, isDeserialize=True, baseURI=None, headers=None, method='GET'):
		if data:
			data = bytes(json.dumps(data), 'utf8')
		req = Request(
				url=(baseURI or self.baseURI)+path,
				headers=self._getHeaders(headers),
				method=method,
				data=data,
				)
		with urlopen(req) as res:
			resBin = res.read()
			if isDeserialize:
				return json.loads(str(resBin, 'utf8'))
			else:
				return resBin

	def _DELETE(self, *args, **nargs):
		return self._GET(*args, method='DELETE', **nargs)

	def _POST(self, path, data, *args, **nargs):
		return self._GET(path, data, *args, method='POST', **nargs)

class Identity(API):
	baseURI = 'https://identity.tyo1.conoha.io'
	token = None
	tenantId = None

	def __init__(self, userName, password, tenantId=None):
		path = '/v2.0/tokens'
		data = { 'auth':{
			'passwordCredentials':{
				'username': userName,
				'password': password,
				},
			}}
		self.tenantId = tenantId
		if tenantId:
			data['auth']['passwordCredentials']['tenantId'] = tenantId
		res = self._POST(path, data)
		self.token = res['access']['token']

	def getTenantId(self):
		return self.tenantId
	def getAuthToken(self):
		return self.token['id']

