
# -*- coding: utf8 -*-
import urllib.request
import json
__ALL__ = 'API Tenant'.split()

class API:
	baseURI = 'https://identity.tyo1.conoha.io'

	def _GET(self, path, baseURI=self.baseURI):
		res = urllib.request.urlopen(baseURI+path).read()
		return json.loads(res)

	def _POST(self, path, data, baseURI=self.baseURI):
		data = json.dujps(data)
		res = urllib.request.urlopen(baseURI+path, data=data).read()
		return json.loads(res)

class Identity(API):
	baseURI = 'https://identity.tyo1.conoha.io'
	token = None

	def getToken(self, userName, password, tenantId=None):
		path = '/v2.0/tokens'
		data = { 'auth':{
			'passwordCredentials':{
				'username': userName,
				'password': password,
				},
			}}
		res = self._POST(path, data)
		self.token = Token(res['access']['token'])

class Token:
	rawData = None
	def __init__(self, jsonToken):
		self.rawData = jsonToken

	def getTenant(self, typeName):
		for tenant in self.rawData['tenant']:
			if tenant['type'] != typeName:
				continue
			return Tenant(tenant['type'])

class Tenant:
	rawData = None

	def __init__(self, jsonTenant):
		self.rawData = jsonTenant

	def getEndpointURI(self, region):
		for endpoint in self.rawData['endpoints']:
			if endpoint['region'] != region:
				continue
			return endpoint['publicURL']

