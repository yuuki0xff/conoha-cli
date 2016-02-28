
from .api import API, CustomList

__all__ = 'BlockType BlockTypeList Volume VolumeList'.split()

class BlockStorageAPI(API):
	def __init__(self, token, baseURIPrefix=None):
		super().__init__(token, baseURIPrefix)
		self._serviceType = 'volume'

class BlockType(BlockStorageAPI):
	def __init__(self, data):
		self.typeId = data['id']
		self.name = data['name']
		self.extra = data['extra_specs']

class BlockTypeList(BlockStorageAPI, CustomList):
	def __init__(self, token):
		super().__init__(token)
		CustomList.__init__(self)
		path = 'types'
		res = self._GET(path)
		self.extend(BlockType(i) for i in res['volume_types'])

	def _getitem(self, key, item):
		return key in [item.typeId, item.name]

class Volume(BlockStorageAPI):
	def __init__(self, data):
		self.volumeId = data['id']
		self.name = data['name']
		self.links = data['links']
		self.attachments = data['attachments']
		self.availability_zone = data['availability_zone']
		self.bootable = data['bootable']
		self.consistencygroup_id = data['consistencygroup_id']
		self.created_at = data['created_at']
		self.description = data['description']
		self.encrypted = data['encrypted']
		self.metadata = data['metadata']
		self.tenantId = data.get('os-vol-tenant-attr:tenant_id')
		self.replication = {
				'driverData': data.get('os-volume-replication:driver_data'),
				'extendedStatus': data.get('os-volume-replication:extended_status'),
				}
		self.replicationStatus = data['replication_status']
		self.size = data['size']
		self.snapshotId = data['snapshot_id']
		self.sourceVolId = data['source_volid']
		self.status = data['status']
		self.userId = data['user_id']
		self.volumeType = data['volume_type']

class VolumeList(BlockStorageAPI, CustomList):
	def __init__(self, token):
		super().__init__(token)
		CustomList.__init__(self)
		path = 'volumes/detail'
		res = self._GET(path)
		self.extend(Volume(i) for i in res['volumes'])

	def _getitem(self, key, item):
		return key in [item.volumeId, item.name]

	def add(self, size, name=None, description=None, source=None, snapshotId=None, imageRef=None, bootable=None, metadata={}):
		assert type(size) is int, TypeError('size must be int type')
		assert size in [200, 500], ValueError('size was 200 or 500')
		if bootable is not None:
			assert type(bootable) is bool, TypeError('bootable must be bool type')
			assert isinstance(metadata, dict), TypeError('metadata must be dict like object')
		if name is not  None:
			assert type(name) is str, TypeError('name must be str type')
			assert len(name) <= 255, ValueError('name was too long')
			assert all(i.isalpha() or i.isnumeric() or (i in '-_') for i in name), ValueError('Invalid name')

		data = {'volume': {
			'source_volid': source,
			'description': description,
			'snapshot_id': snapshotId,
			'size': size,
			'name': name,
			'imageRef': imageRef,
			'bootable': bootable,
			'metadata': metadata,
			}}
		res = self._POST('volumes', data)
		vol = Volume(res['volume'])
		self.append(vol)
		return vol.volumeId

	def delete(self, volumeId):
		res = self._DELETE('volumes/'+volumeId, isDeserialize=False)

	def save(self, volumeId): pass # TODO: image.pyの実装が完了したら、実装する

