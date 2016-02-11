#!/usr/bin/env python3
# -*- coding: utf8 -*-
from conoha.api import Token
from conoha.config import Config
from argparse import ArgumentParser, FileType
import sys
from conoha.compute import VMPlanList, VMImageList, VMList, KeyList
from conoha.network import SecurityGroupList
from tabulate import tabulate
import functools

formatters = ('plain', 'simple', 'vertical')

def prettyPrint(format_=None, header=True):
	"""
	2つの引数(token, args)を取るクラスメソッドに対するデコレータ。
	メソッドが返す値を整形してstdoutに出力する。

	format_: 表示形式を選択
	heder:   ヘッダーの有無を指定

	注意: wrapperの引数 "args" の設定が優先される。
	"""
	assert(format_ is None or format_ in ['plain', 'simple'])

	def verticalFormatter(table, header_):
		headerRow = list(next(table))
		headerWidth = max(len(i) for i in headerRow) if header_ else 0
		spaceWidth = 2 if header_ else 0
		valueColWidth = 0
		rows = 0
		rowsWidth = None
		output = []
		outputStr = ""

		for rowNo, row in enumerate(table):
			# rowの値をすべて文字列に変換
			row = list(str(i) for i in row)

			rows = rowNo
			valueColWidth = max([valueColWidth, max(len(i) for i in row),])
			# 縦横を逆に
			if header_:
				output.append(zip(headerRow, row))
			else:
				output.append(row)
		rowsWidth = len(str(rows))
		separateStr = '*'*(int((headerWidth + spaceWidth + valueColWidth - 2 - rowsWidth)/2))
		for rowNo, row in enumerate(output):
			outputStr += ' '.join([separateStr, str(rowNo).center(rowsWidth), separateStr]) + '\n'
			if header_:
				outputStr += '\n'.join(h.ljust(headerWidth) + ' '*spaceWidth + v for h,v in row) + '\n'
			else:
				outputStr += '\n'.join(row) + '\n'
		return outputStr

	def receiveFunc(func):
		@functools.wraps(func)
		def wrapper(cls, token, args):
			output = func(cls, token, args)
			if output:
				# Select first non None value
				fmt = next((i for i in [args.format, format_] if i is not None), None)
				header_ = next((i for i in [args.header, header] if i is not None), True)
				assert(fmt is None or fmt in formatters)

				if fmt == 'vertical':
					# use verticalFormatter
					print(verticalFormatter(output, header_))
				else:
					# use tabulate
					if header_:
						print(tabulate(output, headers='firstrow', tablefmt=fmt or 'simple'))
					else:
						output = iter(output)
						# Skipt first line
						next(output)
						print(tabulate(output, headers=[], tablefmt=fmt or 'plain'))
		return wrapper
	return receiveFunc

def str2bool(s):
	if s.lower() in ['yes', 'y', 'true', 't', '1']:
		return True
	elif s.lower() in ['no', 'n', 'false', 'f', '0']:
		return False
	raise '"{}" is invalid value'.format(s)

def main():
	parser = getArgumentParser()
	try:
		parsed_args = parser.parse_args()
		# サブコマンドだけを指定した場合は失敗
		assert('func' in parsed_args)
	except AssertionError:
		# 失敗した場合は、そのサブコマンドに対応するhelpを表示
		parser.parse_args(sys.argv[1:]+['-h'])
		return

	conf = Config()
	token = Token(conf)
	parsed_args.func(token, parsed_args)

def getArgumentParser():
	parser = ArgumentParser()
	parser.add_argument('--format', type=str, choices=formatters)
	parser.add_argument('--header', nargs='?', default=True, type=str2bool, choices=[True, False])
	subparser = parser.add_subparsers()

	parser_compute = subparser.add_parser('compute')
	subparser_compute = parser_compute.add_subparsers()
	ComputeCommand.configureParser(subparser_compute)

	parser_network = subparser.add_parser('network')
	subparser_network = parser_network.add_subparsers()
	NetworkCommand.configureParser(subparser_network)

	return parser

class ComputeCommand():
	@classmethod
	def configureParser(cls, subparser):
		listCommands = {
				'list-images': cls.list_images,
				'list-keys': cls.list_keys,
				'list-plans': cls.list_plans,
				'list-vms': cls.list_vms,
				}
		for cmd in listCommands:
			listParser = subparser.add_parser(cmd)
			listParser.add_argument('--verbose', action='store_true')
			listParser.set_defaults(func=listCommands[cmd])

		addKeyParser = subparser.add_parser('add-key')
		addKeyParser.add_argument('--quiet', action='store_true')
		addKeyParser.add_argument('--name', type=str)
		addKeyParser.add_argument('--file', type=FileType('r'))
		addKeyParser.add_argument('--key', type=str)
		addKeyParser.set_defaults(func=cls.add_key)

		deleteKeyParser = subparser.add_parser('delete-key')
		deleteKeyParser.add_argument('--name', type=str)
		deleteKeyParser.set_defaults(func=cls.delete_key)

		addVmParser = subparser.add_parser('add-vm')
		addVmParser.add_argument('--quiet', action='store_true')
		addVmParser.add_argument('--name', type=str)        # for backward compatibility
		addVmParser.add_argument('--image', type=str)
		addVmParser.add_argument('--imageid', type=str)     # for backward compatibility
		addVmParser.add_argument('--plan', type=str)
		addVmParser.add_argument('--planid', type=str)      # for backward compatibility
		addVmParser.add_argument('--passwd', type=str)
		addVmParser.add_argument('--key', type=str)
		addVmParser.add_argument('--group-names', type=str)
		addVmParser.set_defaults(func=cls.add_vm)

		vmCommands = {
				'start-vm': cls.start_vm,
				'stop-vm': cls.stop_vm,
				'reboot-vm': cls.reboot_vm,
				'modify-vm': cls.modify_vm,
				'delete-vm': cls.delete_vm,
				}
		for cmd in vmCommands:
			vmParser = subparser.add_parser(cmd)
			vmParser.add_argument('--name', type=str)
			vmParser.add_argument('--id', type=str)
			if cmd == 'stop-vm':
				vmParser.add_argument('--force', action='store_true')
			elif cmd == 'modify-vm':
				vmParser.add_argument('--planid', type=str)
			vmParser.set_defaults(func=vmCommands[cmd])

	@classmethod
	@prettyPrint()
	def list_plans(cls, token, args):
		plans = VMPlanList(token)
		yield ['ID', 'Name', 'Disk', 'RAM', 'CPUs']
		for p in plans:
			yield [p.planId, p.name, p.disk, p.ram, p.vcpus]

	@classmethod
	@prettyPrint()
	def list_images(cls, token, args):
		imageList = VMImageList(token)
		# Headers
		if args.verbose:
			yield ['ID', 'Name', 'MinDisk', 'MinRam', 'Progress', 'Status', 'Created', 'Updated']
		else:
			yield ['ID', 'Name', 'Status', 'Created', 'Updated']
		# Body
		for img in imageList:
			if args.verbose:
				yield [img.imageId, img.name, img.minDisk, img.minRam, img.progress, img.status, img.created, img.updated]
			else:
				yield [img.imageId, img.name, img.status, img.created, img.updated]

	@classmethod
	@prettyPrint()
	def list_keys(cls, token, args):
		keylist = KeyList(token)
		# Header
		if args.verbose:
			yield ['Name', 'PublicKey', 'FingerPrint']
		else:
			yield ['Name', 'FingerPrint']
		# Body
		for key in keylist:
			if args.verbose:
				yield [key.name, key.publicKey, key.fingerprint]
			else:
				yield [key.name, key.fingerprint]

	@classmethod
	@prettyPrint()
	def list_vms(cls, token, args):
		vmlist = VMList(token)
		# Header
		if args.verbose:
			yield ['VMID', 'FlavorID', 'HostID', 'ImageID', 'TenantID', 'Name', 'Status', 'Created', 'Updated', 'AddressList', 'SecuretyGroupList']
		else:
			yield ['VMID', 'Name', 'Status']
		# Body
		for vm in vmlist:
			if args.verbose:
				yield [vm.vmid, vm.flavorId, vm.hostId, vm.imageId, vm.tenantId, vm.name, vm.status, vm.created, vm.updated, vm.addressList, vm.securityGroupList]
			else:
				yield [vm.vmid, vm.name, vm.status]

	@classmethod
	@prettyPrint()
	def add_key(cls, token, args):
		keylist = KeyList(token)
		keylist.add(name=args.name, publicKey=args.key, publicKeyFile=args.file)

	@classmethod
	@prettyPrint()
	def delete_key(cls, token, args):
		keylist = KeyList(token)
		keylist.delete(args.name)

	@classmethod
	@prettyPrint()
	def add_vm(cls, token, args):
		groupNames = args.group_names and args.group_names.split(',')

		vmlist = VMList(token)
		vmid = vmlist.add(
				args.imageid or vmlist[args.image].imageid,
				args.planid or vmlist[args.plan].planid,
				adminPass=args.passwd,
				keyName=args.key,
				name=args.name,
				securityGroupNames=groupNames)
		if not args.quiet:
			yield 'VMID'
			yield vmid

	@classmethod
	@prettyPrint()
	def start_vm(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vm.start()

	@classmethod
	@prettyPrint()
	def stop_vm(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vm.stop(args.force)

	@classmethod
	@prettyPrint()
	def reboot_vm(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vm.restart()

	@classmethod
	@prettyPrint()
	def delete_vm(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vmlist.delete(vm.vmid)

	@classmethod
	@prettyPrint()
	def modify_vm(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vm.resize(args.planid)

class NetworkCommand():
	@classmethod
	def configureParser(cls, subparser):
		listSG = subparser.add_parser('list-security-groups')
		listSG.add_argument('--verbose', action='store_true')
		listSG.set_defaults(func=cls.listSecurityGroups)

		addSG = subparser.add_parser('add-security-group')
		addSG.add_argument('--name', type=str)
		addSG.add_argument('--description', type=str)
		addSG.set_defaults(func=cls.addSecurityGroup)

		delSG = subparser.add_parser('delete-security-group')
		delSG.add_argument('--name', type=str)
		delSG.add_argument('--id', type=str)
		delSG.set_defaults(func=cls.deleteSecurityGroup)

		listRules = subparser.add_parser('list-rules')
		listRules.add_argument('--verbose', action='store_true')
		listRules.add_argument('--group', type=str)
		listRules.add_argument('--id', type=str)        # for backward compatibility
		listRules.add_argument('--name', type=str)      # for backward compatibility
		listRules.set_defaults(func=cls.listRules)

		addRule = subparser.add_parser('add-rule')
		addRule.add_argument('--group', type=str)
		addRule.add_argument('--id', type=str)          # for backward compatibility
		addRule.add_argument('--direction', type=str)
		addRule.add_argument('--ethertype', type=str)
		addRule.add_argument('--port', type=str)
		addRule.add_argument('--protocol', type=str)
		addRule.add_argument('--remoteIPPrefix', type=str)
		addRule.set_defaults(func=cls.addRule)

		delRule = subparser.add_parser('delete-rule')
		delRule.add_argument('--group', type=str)
		delRule.add_argument('--group-id', type=str)    # for backward compatibility
		delRule.add_argument('--rule-id', type=str)
		delRule.set_defaults(func=cls.deleteRule)

	@classmethod
	@prettyPrint()
	def listSecurityGroups(cls, token, args):
		sglist = SecurityGroupList(token)
		# Header
		yield ['ID', 'Name', 'Description']
		# Body
		for sg in sglist:
			yield [sg.id_, sg.name, sg.description]

	@classmethod
	@prettyPrint()
	def addSecurityGroup(cls, token, args):
		sglist = SecurityGroupList(token)
		id_ = sglist.add(args.name, args.description)
		print(id_)

	@classmethod
	@prettyPrint()
	def deleteSecurityGroup(cls, token, args):
		sglist = SecurityGroupList(token)
		sg = sglist.getSecurityGroup(sgid=args.id, name=args.name)
		sglist.delete(sg.id_)

	@classmethod
	@prettyPrint()
	def listRules(cls, token, args):
		sglist = SecurityGroupList(token)
		sg = sglist[args.group or args.id or args.name]

		# Header
		if args.verbose:
			yield ['ID', 'Direction', 'EtherType', 'RangeMin', 'RangeMax', 'Protocol', 'RemoteIPPrefix']
		else:
			yield ['Direction', 'EtherType', 'RangeMin', 'RangeMax', 'Protocol', 'RemoteIPPrefix']
		# Body
		for rule in sg.rules:
			if args.verbose:
				yield [rule.id_, rule.direction, rule.ethertype, rule.rangeMin, rule.rangeMax, rule.protocol, rule.remoteIPPrefix]
			else:
				yield [rule.direction, rule.ethertype, rule.rangeMin, rule.rangeMax, rule.protocol, rule.remoteIPPrefix]

	@classmethod
	@prettyPrint()
	def addRule(cls, token, args):
		sglist = SecurityGroupList(token)
		sg = sglist[args.group or args.id]

		portMin = None
		portMax = None
		if args.port:
			if ',' in args.port:
				portMin, portMax = args.port.split(',')
			else:
				portMin = portMax = args.port

		sg.rules.add(args.direction, args.ethertype, portMin, portMax, args.protocol, args.remoteIPPrefix)

	@classmethod
	@prettyPrint()
	def deleteRule(cls, token, args):
		sglist = SecurityGroupList(token)
		sg = sglist[args.group or args.group_id]
		sg.rules.delete(args.rule_id)

if __name__ == '__main__':
	exit(main())

