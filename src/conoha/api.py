
# -*- coding: utf8 -*-
from urllib.request import Request, urlopen
import json
__ALL__ = 'API Tenant'.split()

class API:
	baseURI = 'https://identity.tyo1.conoha.io'

	def _getHeaders(self):
		headers={
				'Accept': 'application/json',
				}
		return headers

	def _GET(self, path, baseURI=None):
		req = Request(
				url=(baseURI or self.baseURI),
				headers=self._getHeaders(),
				)
		with urlopen(req) as res:
			return json.loads(res.read())

	def _POST(self, path, data, baseURI=None):
		data = bytes(json.dumps(data), 'utf8')
		req = Request(
				url=(baseURI or self.baseURI)+path,
				data=data,
				method='POST',
				headers=self._getHeaders(),
				)
		with urlopen(req) as res:
			return json.loads(str(res.read(), 'utf8'))

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

