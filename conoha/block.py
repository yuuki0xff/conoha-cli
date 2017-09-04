
import string

from .api import API, CustomList
from .image import Image
from . import error

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
	def __init__(self, data, token):
		super().__init__(token)
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

	def save(self, imageName, diskFormat='qcow2', containerFormat='ovf'):
		"""ボリュームのイメージを保存"""
		# TODO: image.pyの実装が完了したら、実装する
		path = 'volumes/{}/action'.format(self.volumeId)
		data = {
				"os-volume_upload_image": {
					"image_name": imageName,
					"disk_format": diskFormat,
					"container_format": containerFormat,
					}
				}
		res = self._POST(path, data)
		return Image(res)

class VolumeList(BlockStorageAPI, CustomList):
	"""ボリュームの一覧"""
	def __init__(self, token):
		super().__init__(token)
		CustomList.__init__(self)
		path = 'volumes/detail'
		res = self._GET(path)
		self.extend(Volume(i, token) for i in res['volumes'])

	def _getitem(self, key, item):
		return key in [item.volumeId, item.name]

	def add(self, size, name=None, description=None, source=None, snapshotId=None, imageRef=None, bootable=None, metadata={}):
		"""ボリュームを追加

		sizeには 200 または 500 を指定する
		nameは255文字以下。使用可能な文字は[a-zA-Z\\-_]
		"""
		self._validateVolumeSize(size)
		if type(bootable) not in [type(None), bool]:
			raise error.TypeError('bootable must be boolean value or None')
		if not isinstance(metadata, dict):
			raise error.TypeError('metadata must be dict like object')
		if name is not None:
			self._validateVolumeName(name)

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
		vol = Volume(res['volume'], self.token)
		self.append(vol)
		return vol.volumeId

	def delete(self, volumeId):
		res = self._DELETE('volumes/'+volumeId, isDeserialize=False)

	@staticmethod
	def _validateVolumeSize(size):
		if type(size) is not int:
			raise error.TypeError('Volume size must be int type.')
		if size not in [200, 500]:
			raise error.ValueError('Volume size is either 200 or 500.')

	@staticmethod
	def _validateVolumeName(name):
		charset = string.ascii_letters + string.digits + '-_'
		if type(name) is not str:
			raise error.TypeError('Volume name must be str type, but got {} type.'.format(type(name)))
		if len(name) < 1:
			raise error.InvalidNameError('Volume name can not empty.')
		if len(name) > 255:
			raise error.InvalidNameError('Volume name is too long. Its length must be between 1 and 255.')
		for c in name:
			if c not in charset:
				raise error.InvalidNameError('Volume name can not use "{}" character. Its can use only alphabet, digit characters, "-" and "_".'.format(c))
