conoha-cli
==========
conoha-cli is a command and Python3 library for [ConoHa](https://www.conoha.jp/) API.

Installation
------------
ln -s $PWD/src/conoha-cli.py ~/bin/conoha-cli

Command Usage
-------------
### Compute Service
conoha-cli compute list-images \[--verbose\]  
conoha-cli compute list-keys \[--verbose\]  
conoha-cli compute list-plans \[--verbose\]  
conoha-cli compute list-vms \[--verbose\]  

conoha-cli compute add-key \[--quiest\] --name NAME \[--file FILE | --key KEY\]  
conoha-cli compute delete-key --name NAME  

conoha-cli compute add-vm \[--quiest\] \[--name NAME\] \[--imageid IMAGE\_ID\] \[--planid PLAN\_ID\] \[--passwd PASSWD\] \[--key KEY\_NAME\]  
conoha-cli compute start-vm  \[--name NAME | --id VM\_ID\]  
conoha-cli compute stop-vm   \[--name NAME | --id VM\_ID\] \[--force\]  
conoha-cli compute reboot-vm \[--name NAME | --id VM\_ID\]  
conoha-cli compute modify-vm \[--name NAME | --id VM\_ID\] \[--planid PLAN\_ID\]  
conoha-cli compute delete-vm \[--name NAME | --id VM\_ID\]  

### Network Service
conoha-cli network list-security-groups \[--verbose\]  
conoha-cli network add-security-groups --name NAME \[--description DESCRIPTION\]  
conoha-cli network delete-security-groups \[--name NAME | --id SECURITY\_GROUP\_ID\]  

conoha-cli network list-rules \[--verbose\] \[--name NAME | --id SECURITY\_GROUP\_ID\]  
conoha-cli network add-rules --id SECURITY\_GROUP\_ID --direction DIRECTION --ethertype ETHERTYPE \[--port MIN,MAX\] \[--protocol PROTOCOL\] \[--remoteIPPrefix IP\_PREFIX\]  
conoha-cli network delete-rules \[--group-id SECURITY\_GROUP\_ID\] \[--rule-id SECURITY\_GROUP\_RULE\_ID\]  

Library Usage
-------------
```
from conoha.API import Token
from conoha.compute import VMList

userName = ''
password = ''
tenantId = ''

token = Token(userName=userName, password=password, tenantId=tenantId)
for vm in VMList(token):
	if vm.getStatus() == 'SHUTOFF':
		vm.start()

```
