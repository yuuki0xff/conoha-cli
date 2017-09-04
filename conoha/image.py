
from .api import API, CustomList
from . import error
from collections import namedtuple

__all__ = 'Image ImageList Quota'.split()

class ImageAPI(API):
	def __init__(self, token, baseURIPrefix=None):
		super().__init__(token, baseURIPrefix)
		self._serviceType = 'image'


class Image(ImageAPI):
	"""保存済みのディスクイメージ"""
	def __init__(self, data):
		self.status = data.get('status')
		self.name = data['name']
		self.tags = data['tags']
		self.container_format = data['container_format']
		self.created_at = data['created_at']
		self.size = data['size']
		self.disk_format = data['disk_format']
		self.updated_at = data['updated_at']
		self.visibility = data['visibility']
		self.imageId = data['id']
		self.min_disk = data['min_disk']
		self.protected = data['protected']
		self.min_ram = data['min_ram']
		self.file = data['file']
		self.checksum = data['checksum']
		self.owner = data['owner']
		self.direct_url = data['direct_url']
		self.hw_qemu_guest_agent = data.get('hw_qemu_guest_agent')
		self.schema = data['schema']

class ImageList(ImageAPI, CustomList):
	"""保存済みのディスクイメージの一覧"""
	def __init__(self, token):
		super().__init__(token)
		CustomList.__init__(self)
		path = 'images'
		res = self._GET(path)
		self.extend(Image(i) for i in res['images'])

	def _getitem(self, key, item):
		return key in [item.imageId, item.name]

	def delete(self, imageId):
		path= 'images/{}'.format(imageId)
		self._DELETE(path, isDeserialize=False)

class Quota(ImageAPI):
	"""保存可能なディスクイメージの合計サイズを制限する
	500GBで指定可能
	"""
	QuotaTuple = namedtuple('QuotaTuple', ['region', 'size'])

	def __init__(self, token):
		super().__init__(token)
		self.update()

	def update(self, res=None):
		if not res:
			res = self._GET('quota')
		for key, value in res['quota'].items():
			self.region = key.split('_')[0]
			self.size = int(value[:-2])

	def set(self, size):
		"""クォータを設定する
		sizeの単位はGB。
		50, 550, 1050, ...のように500GB単位で設定可能
		"""
		self._validateSize(size)

		data = {'quota': {
			self.region+'_image_size': str(size)+'GB'
			}}

		res = self._PUT('quota', data)
		self.update(res)

	@staticmethod
	def _validateSize(size):
		if type(size) is not int:
			raise error.InvalidSizeError('Size must be int type, but got {} type.'.format(type(size)))
		if not(size >= 50 and (size-50)%500 == 0):  # size: 50, 550, 1050, ...
			raise error.InvalidSizeError('Size must choice of 50, 550, 1050, ...')
