
from .api import API, CustomList

__all__ = "VMPlan VMPlanList VMImage VMImageList VMList VM KeyList Key".split()

class ComputeAPI(API):
	def __init__(self, token, baseURIPrefix=None):
		super().__init__(token, baseURIPrefix)
		self._serviceType = 'compute'

class VMPlan(ComputeAPI):
	"""Compute Serviceのプラン

	インスタンス変数
		planId : str :
		name   : str :
		disk   : int : rootのディスクサイズ
		ram    : int : RAMのサイズ(MiB)
		vcpus  : int : 仮想マシンのCPU数
	"""
	def __init__(self, data):
		self.planId = data['id']
		self.name = data['name']
		self.disk = data['disk']
		self.ram = data['ram']
		self.vcpus = data['vcpus']

class VMPlanList(ComputeAPI, CustomList):
	"""Compute Serviceのプランの一覧を管理する
	データの更新は、オプジェクトが作成された時の1回のみ

	使い方:
	    plans = VMPlanList(token)
	    plan = plans['planName']
	    plan = plans['planId']
	"""
	def __init__(self, token):
		super().__init__(token)
		CustomList.__init__(self)
		path = 'flavors/detail'
		res = self._GET(path)
		self.extend(VMPlan(i) for i in res['flavors'])

	def _getitem(self, key, item):
		return key in [item.planId, item.name]

class VMImage(ComputeAPI):
	"""Compute Serviceのディスクイメージ

	インスタンス変数
		imageId  : str :
		name     : str :
		minDisk  : int : このイメージを使用するために必要な最小のディスクサイズ
		minRam   : int : このイメージを使用するために必要な最小のRAMサイズ
		progress : int :
		status   : str :
		created  : str :
		updated  : str :
	"""
	def __init__(self, data):
		self.imageId = data['id']
		self.name = data['name']
		self.minDisk = data['minDisk']
		self.minRam = data['minRam']
		self.progress = data['progress']
		self.status = data['status']
		self.created = data['created']
		self.updated = data['updated']

class VMImageList(ComputeAPI, CustomList):
	"""保存済みのディスクイメージの一覧

	使い方:
		images = VMImageList(token)
		image = images['imageName']
		image = images['imageId']
	"""
	def __init__(self, token):
		super().__init__(token)
		CustomList.__init__(self)
		path = 'images/detail'
		res = self._GET(path)
		self.extend(VMImage(i) for i in res['images'])

	def _getitem(self, key, item):
		return key in [item.imageId, item.name]

class VMList(ComputeAPI, CustomList):
	"""VMの一覧

	使い方:
	    vms = VMList(token)
	    vm = vms['vmName']
	    vm = vms['vmid']
	"""
	def __init__(self, token):
		super().__init__(token)
		CustomList.__init__(self)
		self.update()

	def _getitem(self, key, item):
		return key in [item.vmid, item.name]

	def update(self):
		"""VMの一覧を更新する"""
		res = self._GET('servers/detail')
		self.clear()
		self.extend(VM(self.token, i) for i in res['servers'])

	def getServer(self, vmid=None, name=None):
		for vm in self:
			if (vmid and vm.vmid == vmid) or (name and vm.name == name):
				return vm

	def add(self, image, flavor, adminPass=None, keyName=None, name=None, securityGroupNames=None):
		data = {'server' : {
				'imageRef' : image,
				'flavorRef' : flavor,
				'metadata': {},
				}}
		if adminPass: data['server']['adminPass'] = adminPass
		if keyName: data['server']['key_name'] = keyName
		if name:
			data['server']['metadata']['instance_name_tag'] = name
		if securityGroupNames:
			data['server']['security_groups'] = []
			for name in securityGroupNames:
				data['server']['security_groups'].append({
					'name': name,
					})

		res = self._POST('servers', data)
		self._servers = None
		return res['server']['id']

	def delete(self, vmid):
		self._DELETE('servers/'+vmid, isDeserialize=False)
		self._servers = None

class VM(ComputeAPI):
	"""仮想マシン
	仮想マシンの状態は、オブジェクトが作成された時点の情報である

	インスタンス変数
		vmid              : str  :
		flavorId          : str  : planのID
		hostId            : str  :
		imageId           : str  :
		tenantId          : str  :
		name              : str  :
		status            : str  :
		created           : str  :
		updated           : str  :
		addressList       : dict :
		securityGroupList : dict :
	"""
	def __init__(self, token, info):
		self.vmid = info['id']
		super().__init__(token, baseURIPrefix='servers/' + self.vmid)
		self.flavorId = info['flavor']['id']
		self.hostId = info['hostId']
		self.imageId = info['image']['id']
		self.tenantId = info['tenant_id']
		try:
			self.name = info['metadata']['instance_name_tag']
		except KeyError:
			self.name = info['name']
		self.status = info['status']
		self.created = info['created']
		self.updated = info['updated']
		self.addressList = info['addresses']
		self.securityGroupList = info['security_groups']

	def _action(self, actionName, actionValue=None):
		action = {actionName: actionValue}
		self._POST('action', action, isDeserialize=False)
	def start(self):
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

class KeyList(ComputeAPI, CustomList):
	"""SSHの鍵の一覧"""
	def __init__(self, token):
		super().__init__(token)
		CustomList.__init__(self)
		self.update()

	def _getitem(self, key, item):
		return key in [item.name, item.fingerprint]

	def update(self):
		"""鍵の一覧を更新する"""
		res = self._GET('os-keypairs')
		self.clear()
		self.extend(Key(keypair['keypair']) for keypair in res['keypairs'])

	def add(self, name, publicKey=None, publicKeyFile=None):
		"""鍵を追加する

		publicKey が文字列なら、そのキーを使用
		publicKeyFile が文字列なら、そのキーを使用
		publicKey or publicKeyFile がfile likeオブジェクトなら、そのキーを使用
		publicKey is None ならば、新しいキーを作成。必ず返されるKey objectからprivateKeyを取得し、保存すること
		"""
		data = {'keypair':{'name': name}}
		keyString = None

		if type(publicKey) is str:
			keyString = publicKey
		elif type(publicKeyFile) is str:
			with open(publicKeyFile) as f:
				keyString = f.read()
		elif (publicKey or publicKeyFile) is not None:
			keyString = (publicKey or publicKeyFile).read()
		else:
			res = self._POST('os-keypairs', data=data)
			return Key(res['keypair'])

		data['keypair']['public_key'] = keyString
		res = self._POST('os-keypairs', data=data)
		self._keys = None
		return Key(res['keypair'])

	def delete(self, keyName):
		"""鍵を削除する
		実行後は update() を実行してください
		"""
		self._DELETE('os-keypairs/'+keyName, isDeserialize=False)
		self._keys = None

class Key(ComputeAPI):
	"""SSHの鍵

	インスタンス変数
		name        : str :
	    fingerprint : str :
		publicKey   : str :
		privateKey  : str : 鍵を作成した時以外はNone
	"""
	def __init__(self, info):
		self.name = info['name']
		self.fingerprint = info['fingerprint']
		self.publicKey = info['public_key']
		self.privateKey = info.get('private_key')

