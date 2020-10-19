
from .api import API, CustomList
from . import error

__all__ = 'Domain DomainList Record RecordList'.split()

class DNSAPI(API):
	def __init__(self, token, baseURIPrefix=None):
		super().__init__(token, baseURIPrefix)
		self._serviceType = 'dns'

	def _getHeaders(self, h):
		headers={
				'Content-Type': 'application/json'
				}
		if h:
			headers.update(h)
		return super()._getHeaders(headers)

class Domain:
	"""ドメイン"""
	def __init__(self, data):
		self.domainId = data['id']
		self.name = data['name']
		self.email = data['email']
		self.serial = data['serial']
		self.gslb = data.get('gslb')
		self.ttl = data['ttl']
		self.description = data['description']
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']

class DomainList(DNSAPI, CustomList):
	"""ドメインの一覧"""
	def __init__(self, token):
		super().__init__(token)
		CustomList.__init__(self)
		path = 'domains'
		res = self._GET(path)
		self.extend(Domain(i) for i in res['domains'])

	def _getitem(self, key, domain):
		return key in [domain.domainId, domain.name]

	def _validateDomain(self, nameOrDomainid):
		domain = self.getDomain(nameOrDomainid)
		if not domain:
			raise error.NotFound('domain', nameOrDomainid)

	def toDomainid(self, nameOrDomainid):
		domain = self.getDomain(nameOrDomainid)
		if domain:
			return domain.domainId

	def toName(self, nameOrDomainid):
		domain = self.getDomain(nameOrDomainid)
		if domain:
			return domain.name

	def getDomain(self, nameOrDomainid):
		if nameOrDomainid:
			for domain in self:
				if (domain.domainId == nameOrDomainid) or (domain.name == nameOrDomainid):
					return domain

	def add(self, name, email, ttl=None, description=None, gslb=None):
		data = {
			'name': name,
			'email': email,
			'ttl': ttl,
			'description': description,
			'gslb': gslb
			}
		res = self._POST('domains', {k: v for k, v in data.items() if v is not None})
		domain = Domain(res)
		self.append(domain)
		return domain

	def update(self, nameOrDomainid, email=None, ttl=None, description=None, gslb=None):
		self._validateDomain(nameOrDomainid)
		domain = self.getDomain(nameOrDomainid)
		data = {
			'email': email,
			'ttl': ttl,
			'description': description,
			'gslb': gslb
			}
		path = 'domains/{}'.format(domain.domainId)
		res = self._PUT(path, {k: v for k, v in data.items() if v is not None})
		self.remove(domain)
		domain = Domain(res)
		self.append(domain)

	def delete(self, nameOrDomainid):
		self._validateDomain(nameOrDomainid)
		domainId = self.toDomainid(nameOrDomainid)
		path = 'domains/{}'.format(domainId)
		self._DELETE(path, isDeserialize=False)

class Record:
	"""レコード"""
	def __init__(self, data):
		self.recordId = data['id']
		self.name = data['name']
		self.domainId = data['domain_id']
		self.type = data['type']
		self.data = data['data']
		self.ttl = data['ttl']
		self.description = data['description']
		self.priority = data['priority']
		self.gslb_check = data.get('gslb_check')
		self.gslb_region = data.get('gslb_region')
		self.gslb_weight = data.get('gslb_weight')
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']

class RecordList(DNSAPI, CustomList):
	"""レコードの一覧"""
	def __init__(self, token, domainId):
		super().__init__(token)
		CustomList.__init__(self)
		path = 'domains/{}/records'.format(domainId)
		res = self._GET(path)
		self.domainId = domainId
		self.extend(Record(i) for i in res['records'])

	def _getitem(self, key, record):
		return key in [record.recordId]

	def _validateRecord(self, recordId):
		recordId = self.getRecord(recordId)
		if not recordId:
			raise error.NotFound('record', recordId)

	def getRecord(self, recordId):
		for record in self:
			if record.recordId == recordId:
				return record

	def add(self, **kwargs):
		path = 'domains/{}/records'.format(self.domainId)
		res = self._POST(path, {k: v for k, v in kwargs.items() if v is not None})
		record = Record(res)
		self.append(record)
		return record

	def update(self, recordId, **kwargs):
		self._validateRecord(recordId)
		record = self.getRecord(recordId)
		path = 'domains/{}/records/{}'.format(self.domainId, recordId)
		res = self._PUT(path, {k: v for k, v in kwargs.items() if v is not None})
		self.remove(record)
		record = Record(res)
		self.append(record)
		return record

	def delete(self, recordId):
		self._validateRecord(recordId)
		record = self.getRecord(recordId)
		path = 'domains/{}/records/{}'.format(record.domainId, record.recordId)
		self._DELETE(path, isDeserialize=False)
		self.remove(record)

