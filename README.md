conoha-cli
==========
conoha-cli is a command and Python3 library for [ConoHa](https://www.conoha.jp/) API.

Installation
------------
from PyPI : ``` pip install conoha-cli ```  
from Source : ``` ./setup.py install ```  

Configuration
-------------
### Environment
```
# ~/.bashrc
export CONOHA_API_USER='xxxxx'
export CONOHA_API_PASSWD='xxxxx'
export CONOHA_API_TENANT='xxxxx'
```

### Config File
```
# ~/.config/conoha/config
[api]
usre = xxxxx
passwd = xxxxx
tenant = xxxxx
```

Command Usage
-------------
Basic Operations:
```bash
$ conoha-cli compute add-vm -w
...

$ conoha-cli compute list-vms
VMID                                  Name          Status    AddressList                                        SecuretyGroupList
------------------------------------  ------------  --------  -------------------------------------------------  -------------------------------------
00000000-0000-0000-0000-000000000000  app1          ACTIVE    111.222.101.11, 2400:8500:1300:800:111:222:101:11  default, gncs-ipv4-all, gncs-ipv6-all
00000000-0000-0000-0000-000000000000  app2          ACTIVE    111.222.102.22, 2400:8500:1300:800:111:222:102:22  default, gncs-ipv4-all, gncs-ipv6-all
00000000-0000-0000-0000-000000000000  app3          ACTIVE    111.222.103.33, 2400:8500:1300:800:111:222:103:33  default, gncs-ipv4-all, gncs-ipv6-all
00000000-0000-0000-0000-000000000000  app4          ACTIVE    111.222.104.44, 2400:8500:1300:700:111:222:104:44  default, gncs-ipv4-all, gncs-ipv6-all
00000000-0000-0000-0000-000000000000  database-srv  ACTIVE    111.222.105.55, 2400:8500:1300:800:111:222:105:55  default, gncs-ipv4-all, gncs-ipv6-all

$ conoha-cli compute start-vm $VM_NAME
$ conoha-cli compute stop-vm $VM_NAME
$ conoha-cli compute delete-vm $VM_NAME
```

Change output format by `--format` and `--header` arguments:
```bash
$ conoha-cli --format plain --header no compute list-vms
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

API Support Status
-------
Service Name             | Status
-------------------------|---------------
Identity Service         | Full Supported
Account Service          | Not Supported
Compute Service          | Partially Supported
Block Storage Service    | Partially Supported
Image Service            | Partially Supported
Network Service          | Partially Supported
Object Storage Service   | Not Supported
Database Hosting Service | Not Supported
DNS Service              | Not Supported
Mail Hosting Service     | Not Supported

See `conoha-apis.md` for deltails.

