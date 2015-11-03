
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
		self._DELETE('servers/'+vmid, isDeserialize=False)

class VM(API):
	baseURI = 'https://compute.tyo1.conoha.io/v2/'
	vmid = None
	name = None

	def __init__(self, identity, info):
		self.baseURI += identity.getTenantId() + '/'
		self.identity = identity
		self.vmid = info['id']
		self.name = info['name']
		self.baseURI += 'servers/' + self.vmid + '/'

	def _action(self, actionName, actionValue=None):
		action = {actionName: actionValue}
		self._POST('action', action, isDeserialize=False)
	def run(self):
		self._action('os-start')
	def stop(self, force=False):
		if force:
			self._action('os-stop', {'force_shutdown': True})
		else:
			self._action('os-stop')
	def restart(self):
		self._action('reboot', {'type': 'SOFT'})
	def resize(self, flavorId):
		self._action('resize', {'flavorRef': flavorId})

class KeyList(API):
	baseURI = 'https://compute.tyo1.conoha.io/v2/'
	keys = None

	def __init__(self, identity):
		self.baseURI += identity.getTenantId() + '/'
		self.identity = identity

	def getKeys(self):
		res = self._GET('os-keypairs')
		self.keys = (keypair['keypair'] for keypair in res['keypairs'])

class Kye(API):
	baseURI = 'https://compute.tyo1.conoha.io/v2/'

	def __init__(self, identity, info):
		self.baseURI += identity.getTenantId() + '/os-keypairs'
		self.identity = identity

