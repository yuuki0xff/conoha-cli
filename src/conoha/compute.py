
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

class VMImages(API):
	baseURI = 'https://compute.tyo1.conoha.io/v2/'
	images = None

	def __init__(self, identity):
		path = identity.getTenantId() + '/images'
		self.identity = identity
		res = self._GET(path)
		self.images = res['images']

class VMList(API):
	baseURI = 'https://compute.tyo1.conoha.io/v2/'
	servers = None

	def __init__(self, identity):
		self.baseURI += identity.getTenantId() + '/'
		self.identity = identity

	def getServers(self):
		res = self._GET('servers')
		self.servers = res['servers']
		return self.servers

	def add(self, image, flavor):
		data = {'server' : {
				'imageRef' : image,
				'flavorRef' : flavor,
				'adminPass' : '(Rasdfjklweiojfdsakl'
				}}
		res = self._POST('servers', data)
		return res['server']['id']

	def delete(self, vmid):
		self._DELETE('servers/'+vmid, isDeserialize=True)

