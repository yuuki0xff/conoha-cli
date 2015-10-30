
from .api import API, Identity

class VMPlans(API):
	baseURI = 'https://compute.tyo1.conoha.io/v2/'
	flavors = None
	identity = None

	def __init__(self, identity):
		path = identity.getTenantId() + '/flavors'
		self.identity = identity
		res = self._GET(path)
		self.flavors = res['flavors']

