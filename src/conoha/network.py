
from .api import API

class NetworkAPI(API):
	baseURI = 'https://networking.tyo1.conoha.io/v2.0/'


class SecurityGroupList(NetworkAPI):
	_groups = None

	def __init__(self, token):
		self.token = token
		self.update()

	def __iter__(self):
		if self._groups is None:
			self.update()

		for g in self._groups:
			yield SecurityGroup(self.token, g)

	def update(self):
		res = self._GET('security-groups')
		self._groups = res['security_groups']

	def add(self, name, description=None):
		data = {'security_group': {
			'name': name,
			'description': description,
			}}
		res = self._POST('security-groups', data)
		return res['security_group']['id']

	def delete(self, securityGroupID):
		self._DELETE('security-groups/{}'.format(securityGroupID), isDeserialize=False)

class SecurityGroup(NetworkAPI):
	id_ = None
	name = None
	description = None
	rules = None

	def __init__(self, token, info):
		self.token = token
		self.id_ = info['id']
		self.name = info['name']
		self.description = info['description']
		self.rules = SecurityGroupRuleList(token, self.id_, info['security_group_rules'])

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

class SecurityGroupRuleList(NetworkAPI):
	securityGroupID = None
	_rules = None

	def __init__(self, token, id_, info):
		self.token = token
		self.securityGroupID = id_
		self._rules = info

	def __iter__(self):
		if self._rules is None:
			self.update()

		for r in self._rules:
			yield SecurityGroupRule(r)

	def update(self): pass
	def add(self, direction, ethertype, portMin=None, portMax=None, protocol=None, remoteIPPrefix=None):
		assert(direction in ['ingress', 'egress'])
		assert(ethertype in ['IPv4', 'IPv6'])
		assert(portMin is None or str(portMin).isdigit())
		assert(portMax is None or str(portMax).isdigit())
		assert(protocol is None or protocol in ['tcp', 'udp', 'icmp', 'null'])

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
	id_ = None
	direction = None
	ethertype = None
	rangeMin = None
	rangeMax = None
	protocol = None
	remoteIPPrefix = None

	def __init__(self, info):
		self.id_ = info['id']
		self.direction = info['direction']
		self.ethertype = info['ethertype']
		self.rangeMin = info['port_range_min']
		self.rangeMax = info['port_range_max']
		self.protocol = info['protocol']
		self.remoteIPPrefix = info['remote_ip_prefix']


