
import builtins

class APIError(Exception): pass

class ValueError(builtins.ValueError, APIError): pass
class InvalidArgumentError(ValueError):
	def __init__(self, reason):
		self.reason = reason

	def __str__(self):
		return str(self.reason)

class InvalidNameError(ValueError): pass
class InvalidPasswordError(ValueError): pass
class InvalidSizeError(ValueError): pass
class NotFound(InvalidNameError):
	def __init__(self, resource_type:str, name:str):
		self.resource = resource_type
		self.name = name

	def __str__(self):
		return 'specified {} not found: {}'.format(self.resource, self.name)

class ImageNotFound(NotFound):
	def __init__(self, name):
		super().__init__('image', name)

class VMNotFound(NotFound):
	def __init__(self, name):
		super().__init__('VM', name)

class TypeError(builtins.TypeError, APIError): pass
