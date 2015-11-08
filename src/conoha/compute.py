
from .api import API, Identity

class ComputeAPI(API):
	baseURI = 'https://compute.tyo1.conoha.io/v2/'

class VMPlan(ComputeAPI):
	planId = None
	name = None
	disk = None
	ram = None
	vcpus = None

	def __init__(self, data):
		self.planId = data['id']
		self.name = data['name']
		self.disk = data['disk']
		self.ram = data['ram']
		self.vcpus = data['vcpus']

class VMPlanList(ComputeAPI):
	_flavors = None

	def __init__(self, identity):
		path = identity.getTenantId() + '/flavors/detail'
		self.identity = identity
		res = self._GET(path)
		self._flavors = res['flavors']

	def __iter__(self):
		for f in self._flavors:
			yield VMPlan(f)

class VMImage(ComputeAPI):
	imageId = None
	name = None
	minDisk = None
	minRam = None
	progress = None
	status = None
	created = None
	updated = None

	def __init__(self, data):
		self.imageId = data['id']
		self.name = data['name']
		self.minDisk = data['minDisk']
		self.minRam = data['minRam']
		self.progress = data['progress']
		self.status = data['status']
		self.created = data['created']
		self.updated = data['updated']

class VMImageList(ComputeAPI):
	_images = None

	def __init__(self, identity):
		path = identity.getTenantId() + '/images/detail'
		self.identity = identity
		res = self._GET(path)
		self._images = res['images']

	def __iter__(self):
		for i in self._images:
			yield VMImage(i)

class VMList(ComputeAPI):
	_servers = None

	def __init__(self, identity):
		self.baseURI += identity.getTenantId() + '/'
		self.identity = identity
		res = self._GET('servers/detail')
		self._servers = res['servers']

	def __iter__(self):
		for v in self._servers:
			yield VM(self.identity, v)

	def getServer(self, vmid):
		res = self._GET('servers/'+vmid)
		return VM(self.identity, res['server'])

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

class VM(ComputeAPI):
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
	def confirmResize(self):
		self._action('confirmResize')
	def revertResize(self):
		self._action('revertResize')
	def getStatus(self):
		res = self._GET('')
		return res['server']['status']

class KeyList(ComputeAPI):
	keys = None

	def __init__(self, identity):
		self.baseURI += identity.getTenantId() + '/'
		self.identity = identity

	def getKeys(self):
		res = self._GET('os-keypairs')
		self.keys = (keypair['keypair'] for keypair in res['keypairs'])

class Kye(ComputeAPI):
	def __init__(self, identity, info):
		self.baseURI += identity.getTenantId() + '/os-keypairs'
		self.identity = identity

