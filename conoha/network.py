
from .api import API, CustomList
from . import error

__all__ = "SecurityGroupList SecurityGroup SecurityGroupRuleList SecurityGroupRule AddressList Addres".split()

class NetworkAPI(API):
	def __init__(self, token, baseURIPrefix=None):
		super().__init__(token, baseURIPrefix)
		self._serviceType = 'network'

class SecurityGroupList(NetworkAPI, CustomList):
	"""セキュリティグループの一覧

	使い方:
	    sgroups = SecurityGroupList(token)
	    sgroup = sgroups['groupName']
	    sgroup = sgroups['groupId']
	"""

	def __init__(self, token, info=None):
		super().__init__(token)
		CustomList.__init__(self)
		self.update(info)

	def _getitem(self, key, item):
		return key in [item.id_, item.name]

	def __str__(self):
		return ', '.join(sorted(grp.name for grp in self))

	def update(self, res=None):
		"""セキュリティグループの一覧を更新する"""
		if res is None:
			res = self._GET('security-groups')
			self.clear()
		else:
			if 'security_groups' not in res:
				# VMの作成直後は、VM一覧からSecurity Groupsを取得できない。
				# このときにクラッシュするのを防止する。
				# TODO: ここでハンドリングするのは良くない。
				return
		self.extend(SecurityGroup(self.token, i) for i in res['security_groups'])

	def getSecurityGroup(self, sgid=None, name=None):
		for sg in self:
			if (sg.id_ == sgid) or (sg.name == name):
				return sg

	def add(self, name, description=None):
		# NOTE: This API seem to have not validation of parameters.
		#       https://www.conoha.jp/docs/neutron-create_secgroup.html
		data = {'security_group': {
			'name': name,
			'description': description,
			}}
		res = self._POST('security-groups', data)
		return res['security_group']['id']

	def delete(self, securityGroupID):
		self._DELETE('security-groups/{}'.format(securityGroupID), isDeserialize=False)

class SecurityGroup(NetworkAPI):
	"""セキュリティグループ

	インスタンス変数:
	    id_         : str                   :
	    name        : str                   :
	    description : str                   :
	    rules       : SecurityGroupRuleList : このグループに属しているルールの一覧
	"""
	def __init__(self, token, info):
		super().__init__(token)
		self.id_ = info.get('id', None)
		self.name = info['name']
		self.description = info.get('description', None)
		if 'security_group_rules' in info:
			self.rules = SecurityGroupRuleList(token, self.id_, info['security_group_rules'])
		else:
			self.rules = None

	def updateName(self, name):
		data = {'security_group': {
			'name': name,
			}}
		self._PUT('security-groups/{}'.format(self.id_), data)

	def updateDescription(self, description):
		data = {'security_group': {
			'description': description,
			}}
		self._PUT('security-groups/{}'.format(self.id_), data)

class SecurityGroupRuleList(NetworkAPI, CustomList):
	"""フィルタリングルールの一覧"""
	def __init__(self, token, id_, info):
		super().__init__(token)
		CustomList.__init__(self)
		self.securityGroupID = id_
		self.extend(SecurityGroupRule(i) for i in info)

	def _getitem(self, key, item):
		return key in [item.id_]

	def update(self): pass
	def add(self, direction, ethertype, portMin=None, portMax=None, protocol=None, remoteIPPrefix=None):
		# validations
		if direction not in ['ingress', 'egress']:
			raise error.ValueError('direction must be either "ingress" or "egress".')
		if ethertype not in ['IPv4', 'IPv6']:
			raise error.ValueError('ethertype must be either "IPv4" or "IPv6".')
		if portMin not in [type(None), int]:
			raise error.ValueError('portMin must be int or None.')
		if portMax not in [type(None), int]:
			raise error.ValueError('portMax must be int or None.')
		if not(protocol is None or protocol in ['tcp', 'udp', 'icmp', 'null']):
			raise error.ValueError('protocol must choice of "tcp", "udp", "icmp" or "null".')

		data = {'security_group_rule':{
			'direction': direction,
			'ethertype': ethertype,
			'security_group_id': self.securityGroupID,
			}}
		if portMin:
			data['security_group_rule']['port_range_min'] = str(portMin)
		if portMax:
			data['security_group_rule']['port_range_max'] = str(portMax)
		if protocol:
			data['security_group_rule']['protocol'] = protocol

		self._POST('security-group-rules', data)

	def delete(self, securityGroupRuleID):
		self._DELETE('security-group-rules/{}'.format(securityGroupRuleID), isDeserialize=False)

class SecurityGroupRule(NetworkAPI):
	"""フィルタリングルール

	インスタンス変数:
	    id_:str:
	    direction      : str         : "ingress" or "egress"
	    ethertype      : str         : "IPv4" or "IPv6"
	    rangeMin       : int or None : 規制するポート番号の下限
	    rangeMax       : int or None : 対象のポート番号の上限
	    protocol       : str or None : "tcp" or "udp" or "icmp" or "null"
	    remoteIPPrefix : str         :
	"""
	def __init__(self, info):
		self.id_ = info['id']
		self.direction = info['direction']
		self.ethertype = info['ethertype']
		self.rangeMin = info['port_range_min']
		self.rangeMax = info['port_range_max']
		self.protocol = info['protocol']
		self.remoteIPPrefix = info['remote_ip_prefix']


class AddressList(CustomList):
	def __init__(self, info):
		CustomList.__init__(self)
		addrinfo = info['addresses']
		keys = list(addrinfo.keys())
		if keys:
			addrlist = addrinfo[keys[0]]
			self.extend(Address(i) for i in addrlist)

	def _getitem(self, key, item):
		return key in [item.id_]

	def __str__(self):
		vms = sorted(self, key=lambda vm: (vm.version, vm.addr))
		return ', '.join(vm.addr for vm in vms)


class Address:
	def __init__(self, info):
		self.version = info['version']
		self.addr = info['addr']
