
import builtins

class APIError(Exception): pass

class ValueError(builtins.ValueError, APIError): pass
class InvalidNameError(ValueError): pass
class InvalidPasswordError(ValueError): pass
class InvalidSizeError(ValueError): pass

class TypeError(builtins.TypeError, APIError): pass
