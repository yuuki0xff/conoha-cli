conoha-cli
==========
conoha-cli is a command and Python3 library for [ConoHa](https://www.conoha.jp/) API.

Support Status
-------
Service Name             | Status
-------------------------|---------------
Identity Service         | Full Support
Account Service          | Not Support
Compute Service          | Some Support
Block Storage Service    | Some Support
Image Service            | Some Support
Network Service          | Some Support
Object Storage Service   | Not Support
Database Hosting Service | Not Support
DNS Service              | Not Support
Mail Hosting Service     | Not Support

See conoha-apis.md for deltails.

Installation
------------
from PIP : ``` pip install conoha-cli ```  
from Source : ``` ./setup.py install ```  

Configuration
-------------
### Environment`
```
# ~/.bashrc
export CONOHA_API_USER='xxxxx'
export CONOHA_API_PASSWD='xxxxx'
export CONOHA_API_TENANT='xxxxx'
```

### Config File
Create file like this to ~/.config/conoha/config.
```
[api]
usre = xxxxx
passwd = xxxxx
tenant = xxxxx
```

Command Usage
-------------
```
$ conoha-cli compute list-vms
$ conoha-cli compute start-vm $VM_NAME
```

Library Usage
-------------
```
from conoha.config import Config
from conoha.api import Token
from conoha.compute import VMList

configDict = {
	'api': {
		'user':   'xxxxx',
		'passwd': 'xxxxx',
		'tenant': 'xxxxx',
	}
}
conf = Config(fromDict=configDict)
token = Token(conf)
for vm in VMList(token):
	if vm.getStatus() == 'SHUTOFF':
		vm.start()
```
