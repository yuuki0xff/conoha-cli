
from .api import API, CustomList
from collections import namedtuple

__all__ = 'Image ImageList Quota'.split()

class ImageAPI(API):
	def __init__(self, token, baseURIPrefix=None):
		super().__init__(token, baseURIPrefix)
		self._serviceType = 'image'


class Image(ImageAPI):
	def __init__(self, data):
		self.status = data['status']
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
		self.hw_qemu_guest_agent = data['hw_qemu_guest_agent']
		self.schema = data['schema']

class ImageList(ImageAPI, CustomList):
	def __init__(self, token):
		super().__init__(token)
		CustomList.__init__(self)
		path = 'images'
		res = self._GET(path)
		self.extend(Image(i) for i in res['images'])

	def _getitem(self, key, item):
		return key in [item.imageId, item.name]

class Quota(ImageAPI):
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
		assert(type(size) is int)
		assert(size >= 50 and (size-50)%500 == 0) # size: 50, 550, 1050, ...

		data = {'quota': {
			self.region+'_image_size': str(size)+'GB'
			}}

		res = self._PUT('quota', data)
		self.update(res)

