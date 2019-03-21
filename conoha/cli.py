#!/usr/bin/env python3
# -*- coding: utf8 -*-
from argparse import FileType
import argparse
import sys
import functools
import typing
import getpass

from tabulate import tabulate

from conoha.api import Token
from conoha.config import Config
import conoha
from conoha.compute import VMPlanList, VMImageList, VMList, KeyList
from conoha.network import SecurityGroupList
from conoha.block import BlockTypeList, VolumeList
from conoha.image import ImageList, Quota
from conoha import error

formatters = ('plain', 'simple', 'vertical')
maxCommandNameLength = 20

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
			if ('quiet' in args) and args.quiet:
					return
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


def main(args=None):
	parser = getArgumentParser()
	if args is None:
		args = sys.argv[1:]

	try:
		parsed_args = parser.parse_args(args)

		if parsed_args.version:
			print('conoha-cli {}'.format(conoha.__version__))
			return 0

		# サブコマンドだけを指定した場合は失敗
		assert('func' in parsed_args)
	except AssertionError:
		# 失敗した場合は、そのサブコマンドに対応するhelpを表示
		try:
			parser.parse_args(sys.argv[1:]+['-h'])
		except SystemExit:
			return 1
		# ここが実行されてはいけない
		return 2

	conf = Config()
	token = Token(conf)
	try:
		parsed_args.func(token, parsed_args)
		return 0
	except error.APIError as e:
		print('ERROR:', e, file=sys.stderr)
		return 3

class HelpFormatter(argparse.HelpFormatter):
	"""
	argparseのデフォルトのhelpフォーマッタ(argparse.HelpFormatter)に下記の点を改良

	 * 長いサブコマンド名をサポート
	 * サブコマンド一覧をソートする
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# 長い名前のサブコマンドが多いから
		self._action_max_length = maxCommandNameLength

	def _format_action(self, action):
		if isinstance(action, argparse._SubParsersAction):
			# サブコマンド一覧を、サブコマンド名でソートする
			action._choices_actions.sort(key=lambda x: x.dest)
			return super()._format_action(action)
		return super()._format_action(action)

class ArgumentParser(argparse.ArgumentParser):
	"""
	argparse.ArgumentParserクラスに下記の変更を加えた

	 * formatterは常にHelpFormatterを使用
	 * subparserは常にArgumentParserを使用
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.formatter_class = HelpFormatter

	def add_subparsers(self, **kwargs):
		kwargs['parser_class'] = type(self)
		kwargs.setdefault('title', 'subcommands')
		kwargs.setdefault('metavar', 'COMMAND')
		return super().add_subparsers(**kwargs)

def getArgumentParser():
	parser = ArgumentParser()
	parser.add_argument('-v', '--version', action='store_true', help='Display conoha-cli version')
	parser.add_argument('--format', type=str, choices=formatters,
			help='FORMAT is ' + ' or '.join("'{}'".format(i) for i in formatters),
			metavar='FORMAT')
	parser.add_argument('--header', nargs='?', default=True, type=str2bool,
			choices=[True, False], metavar='Yes,No')
	subparser = parser.add_subparsers()

	parser_compute = subparser.add_parser('compute', help='Compute service')
	subparser_compute = parser_compute.add_subparsers()
	ComputeCommand.configureParser(subparser_compute)

	parser_network = subparser.add_parser('network', help='Network service')
	subparser_network = parser_network.add_subparsers()
	NetworkCommand.configureParser(subparser_network)

	parser_block = subparser.add_parser('block', help='Block storage service')
	subparser_block = parser_block.add_subparsers()
	BlockCommand.configureParser(subparser_block)

	parser_image = subparser.add_parser('image', help='Image service')
	subparser_image = parser_image.add_subparsers()
	ImageCommand.configureParser(subparser_image)

	return parser

class ComputeCommand:
	@classmethod
	def configureParser(cls, subparser):
		listCommands = {
				'list-images': cls.list_images,
				'list-keys': cls.list_keys,
				'list-plans': cls.list_plans,
				'list-vms': cls.list_vms,
				}
		for cmd in listCommands:
			listParser = subparser.add_parser(cmd, help='')
			listParser.add_argument('--verbose', action='store_true')
			listParser.set_defaults(func=listCommands[cmd])

		addKeyParser = subparser.add_parser('add-key', help='add public key')
		addKeyParser.add_argument('-q', '--quiet', action='store_true')
		addKeyParser.add_argument('-n', '--name', required=True, type=str,           help='public key name')
		addKeyParser.add_argument('-f', '--file',                type=FileType('r'), help='public key file path')
		addKeyParser.add_argument('-k', '--key',                 type=str,           help='public key string')
		addKeyParser.set_defaults(func=cls.add_key)

		deleteKeyParser = subparser.add_parser('delete-key', help='delete public key')
		deleteKeyParser.add_argument('-n', '--name', type=str, help='key name')
		deleteKeyParser.set_defaults(func=cls.delete_key)

		addVmParser = subparser.add_parser('add-vm', help='add VM')
		addVmParser.add_argument('-w', '--wizard', action='store_true', help='enable wizard mode')
		addVmParser.add_argument('-q', '--quiet', action='store_true', help='trun off output')
		addVmParser.add_argument('-n', '--name',        type=str, help='VM name')         # for backward compatibility
		addVmImageGroup = addVmParser.add_mutually_exclusive_group()
		addVmImageGroup.add_argument('-i', '--image',   type=str, help='image name or image id')
		addVmImageGroup.add_argument('-I', '--imageid', type=str, help='image id')        # for backward compatibility
		addVmPlanGroup = addVmParser.add_mutually_exclusive_group()
		addVmPlanGroup.add_argument('-p', '--plan',     type=str, help='plan name or plan id')
		addVmPlanGroup.add_argument('-P', '--planid',   type=str, help='plan id')         # for backward compatibility
		addVmParser.add_argument(      '--passwd',      type=str, help='root user password')
		addVmParser.add_argument('-k', '--key',         type=str, help='public key name')
		addVmParser.add_argument('-g', '--group-names', type=str, help='security group name')
		addVmParser.set_defaults(func=cls.add_vm)

		vmCommands = {
				'start-vm' :    {'func': cls.start_vm,     'help': 'start VM'},
				'stop-vm':      {'func': cls.stop_vm,      'help': 'stop VM'},
				'reboot-vm':    {'func': cls.reboot_vm,    'help': 'reboot VM'},
				'modify-vm':    {'func': cls.modify_vm,    'help': 'change plan'},
				'delete-vm':    {'func': cls.delete_vm,    'help': 'delete VM'},
				'create-image': {'func': cls.create_image, 'help': 'save local disk'},
				}
		for cmd in vmCommands:
			vmParser = subparser.add_parser(cmd, help=vmCommands[cmd]['help'])
			vmParser.add_argument('-n', '--name', type=str, help='VM name (obsolete)')
			vmParser.add_argument('-i', '--id',   type=str, help='VM id (obsolete)')

			if cmd not in ['create-image']:
				vmParser.add_argument('names', type=str, nargs='*', metavar='NAME', help='ID or name')
			else:
				vmParser.add_argument('names', type=str, nargs='?', metavar='NAME', help='ID or name')

			if cmd == 'stop-vm':
				vmParser.add_argument('-f', '--force', action='store_true')
			elif cmd == 'modify-vm':
				vmParser.add_argument('-P', '--planid', type=str, help='plan id')
			elif cmd == 'create-image':
				vmParser.add_argument('-I', '--image-name', type=str, help='Image name')
			vmParser.set_defaults(func=vmCommands[cmd]['func'])

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
			yield ['VMID', 'Name', 'Status', 'AddressList', 'SecuretyGroupList']
		# Body
		for vm in vmlist:
			if args.verbose:
				yield [vm.vmid, vm.flavorId, vm.hostId, vm.imageId, vm.tenantId, vm.name, vm.status, vm.created, vm.updated, vm.addressList, vm.securityGroupList]
			else:
				yield [vm.vmid, vm.name, vm.status, vm.addressList, vm.securityGroupList]

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
		if args.wizard:
			# name
			default_name = args.name
			prompt = 'Name [L to list exists VM names]: '
			if default_name:
				prompt = 'Name [default: {},  L to list exists VM names]: '.format(default_name)
			while True:
				args.name = input(prompt)
				if args.name == 'L':
					main(['compute', 'list-vms'])
					continue
				if args.name == '':
					args.name = default_name or None
				break

			# image
			images = VMImageList(token)
			default_image = args.imageid or args.image
			if not default_image:
				default_image = images[0].name
				for img in images:
					if '-docker-' in img.name and img.name.endswith('-amd64'):
						# The img.name will be match this pattern.
						# 'vmi-docker-xx.xx-ubuntu-xx.xx-amd64'
						default_image = img.name
						break
			while True:
				args.image = input('Base Image [default: {},  L to list images]: '.format(default_image))
				if args.image == 'L':
					main(['compute', 'list-images'])
					continue
				if args.image == '':
					args.image = default_image
				try:
					args.imageid = images[args.image].imageId
					break
				except KeyError:
					print('ERROR: Invalid image name. See the image list.')
					continue

			# plans
			plans = VMPlanList(token)
			default_plan = args.planid or args.plan or 'g-2gb'
			while True:
				args.plan = input('Plan [default: {},  L to list plans]: '.format(default_plan))
				if args.plan == 'L':
					main(['compute', 'list-plans'])
					continue
				if args.plan == '':
					args.plan = default_plan
				try:
					args.planid = plans[args.plan].planId
					break
				except KeyError:
					print('ERROR: Invalid plan name. See the plan list.')
					continue

			# password
			if not args.passwd:
				while True:
					passwd1 = getpass.getpass('Password: ')
					passwd2 = getpass.getpass('Confirm Password: ')
					if passwd1 == passwd2:
						args.passwd = passwd1
						break
					else:
						print('ERROR: Password does not match. Please re-enter the password again.')
			else:
				print('Password: ***** (masked)')

			# SSH Public Key
			keys = KeyList(token)
			default_key = args.key
			if not args.key:
				if len(keys):
					default_key = keys[0].name
			if default_key:
				while True:
					args.key = input(
						'SSH Public Key [default: {},  L to list keys, None to unspecified the key]: '.format(
							default_key))
					if args.key == 'L':
						main(['compute', 'list-keys'])
						continue
					if args.key == 'None':
						args.key = None
						break
					if args.key == '':
						args.key = default_key
					try:
						_ = keys[args.key]
						break
					except KeyError:
						print('ERROR: invalid key name. See the key list')
						continue
			else:
				# 公開鍵が登録されていない
				args.key = None

			# Security Groups
			default_groups = args.group_names or 'default, gncs-ipv4-all, gncs-ipv6-all'
			while True:
				args.group_names = input('Security Groups [default: {},  L to list groups]: '.format(default_groups))
				if args.group_names == 'L':
					main(['network', 'list-security-groups'])
					continue
				if args.group_names == '':
					args.group_names = default_groups
				break
		else:
			if not any([args.imageid, args.image]):
				raise error.InvalidArgumentError('one of the arguments --image or --imageid is required.')
			if not any([args.planid, args.plan]):
				raise error.InvalidArgumentError('one on the arguments --plan or --planid is required.')

		groupNames = None
		if args.group_names.strip():
			groupNames = [group.strip() for group in args.group_names.strip().split(',')]

		vmlist = VMList(token)
		vmid = vmlist.add(
				args.imageid or VMImageList(token)[args.image].imageId,
				args.planid or VMPlanList(token)[args.plan].planId,
				adminPass=args.passwd,
				keyName=args.key,
				name=args.name,
				securityGroupNames=groupNames)
		if not args.quiet:
			yield ['VMID']
			yield [vmid]

	@classmethod
	@prettyPrint()
	def start_vm(cls, token, args):
		for vm in cls._vmlist(token, args):
			vm.start()

	@classmethod
	@prettyPrint()
	def stop_vm(cls, token, args):
		for vm in cls._vmlist(token, args):
			vm.stop(args.force)

	@classmethod
	@prettyPrint()
	def reboot_vm(cls, token, args):
		for vm in cls._vmlist(token, args):
			vm.restart()

	@classmethod
	@prettyPrint()
	def delete_vm(cls, token, args):
		vmlist = VMList(token)
		for vm in cls._vmlist(token, args):
			vmlist.delete(vm.vmid)

	@classmethod
	@prettyPrint()
	def modify_vm(cls, token, args):
		for vm in cls._vmlist(token, args):
			vm.resize(args.planid)

	@classmethod
	def create_image(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vm.createImage(args.image_name)

	@classmethod
	def _vmlist(cls, token, args)->typing.Iterable[conoha.compute.VM]:
		vmlist = VMList(token)
		if args.names:
			for name in args.names:
				vm = vmlist.getServer(vmid=name, name=name)
				if vm is None:
					raise error.VMNotFound(name)
				yield vm
		elif args.id or args.name:
			vm = vmlist.getServer(vmid=args.id, name=args.name)
			if vm is None:
				raise error.VMNotFound(args.id or args.name)
			yield vm
		else:
			raise error.InvalidArgumentError('argument is not specified: must specify the --name, --id or NAME positional argument')

class NetworkCommand:
	@classmethod
	def configureParser(cls, subparser):
		listSG = subparser.add_parser('list-security-groups', help='')
		listSG.add_argument('-v', '--verbose', action='store_true', help='be verbose')
		listSG.set_defaults(func=cls.listSecurityGroups)

		addSG = subparser.add_parser('add-security-group', help='add security group')
		addSG.add_argument('-n', '--name',        type=str)
		addSG.add_argument('-d', '--description', type=str)
		addSG.set_defaults(func=cls.addSecurityGroup)

		delSG = subparser.add_parser('delete-security-group', help='delete security group')
		delSG.add_argument('-n', '--name', type=str)
		delSG.add_argument('-i', '--id',   type=str)
		delSG.set_defaults(func=cls.deleteSecurityGroup)

		listRules = subparser.add_parser('list-rules', help='display the packet filtering rules in security group')
		listRules.add_argument('-v', '--verbose', action='store_true')
		listRules.add_argument('-g', '--group', type=str, help='security group name or ID')
		listRules.add_argument('-i', '--id',    type=str, help='security group ID')        # for backward compatibility
		listRules.add_argument('-n', '--name',  type=str, help='security group name')      # for backward compatibility
		listRules.set_defaults(func=cls.listRules)

		addRule = subparser.add_parser('add-rule', help='add packet filtering rule')
		addRule.add_argument('-g', '--group',          type=str, help='security group name or ID')
		addRule.add_argument('-i', '--id',             type=str, help='security group ID') # for backward compatibility
		addRule.add_argument('-d', '--direction',      type=str, help='"ingress" or "egress"')
		addRule.add_argument('-e', '--ethertype',      type=str, help='ipv4 or ipv6')
		addRule.add_argument('-p', '--port',           type=str, help='port number')
		addRule.add_argument('-P', '--protocol',       type=str, help='tcp or tdp or icmp')
		addRule.add_argument('-r', '--remoteIPPrefix', type=str, metavar='REMOTE_IP')
		addRule.set_defaults(func=cls.addRule)

		delRule = subparser.add_parser('delete-rule', help='delete packet filtering rule')
		delRule.add_argument('-g', '--group',     type=str, help='security group name or ID')
		delRule.add_argument('-G', '--group-id',  type=str, help='security group ID') # for backward compatibility
		delRule.add_argument('-r', '--rule-id',   type=str, help='packet filtering rule ID')
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
		rules = sg is not None and sg.rules or []
		for rule in rules:
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

class BlockCommand:
	@classmethod
	def configureParser(cls, subparser):
		listTypes = subparser.add_parser('list-types', help='display volume types')
		listTypes.add_argument('-v', '--verbose', action='store_true', help='be verbose')
		listTypes.set_defaults(func=cls.listTypes)

		listVolumes = subparser.add_parser('list-volumes', help='list volumes')
		listVolumes.add_argument('-v', '--verbose', action='store_true', help='be verbose')
		listVolumes.set_defaults(func=cls.listVolumes)

		addVolume = subparser.add_parser('add-volume', help='add a volume')
		addVolume.add_argument('-q', '--quiet', action='store_true', help='trun off output')
		addVolume.add_argument('-s', '--size',        type=int,      help='200 or 500 GiB')
		addVolume.add_argument('-n', '--name',        type=str,      help='volume name')
		addVolume.add_argument('-d', '--description', type=str)
		addVolume.add_argument('-S', '--source',      type=str)
		addVolume.add_argument(      '--snapshotId',  type=str)
		addVolume.add_argument('-i', '--image-ref',   type=str)
		addVolume.add_argument('-b', '--bootable', action='store_true')
		addVolume.set_defaults(func=cls.addVolume)

		deleteVolume = subparser.add_parser('delete-volume', help='delete a volume')
		deleteVolume.add_argument('-n', '--name', type=str,  help='volume name')
		deleteVolume.add_argument('-i', '--id',   type=str,  help='volume ID')
		deleteVolume.set_defaults(func=cls.deleteVolume)

	@classmethod
	@prettyPrint()
	def listTypes(cls, token, args):
		typeList = BlockTypeList(token)
		# Header
		if args.verbose:
			yield ['ID', 'Name', 'Description']
		else:
			yield ['ID', 'Name']
		# Body
		for type_ in typeList:
			if args.verbose:
				yield [type_.typeId, type_.name, type_.extra]
			else:
				yield [type_.typeId, type_.name]

	@classmethod
	@prettyPrint()
	def listVolumes(cls, token, args):
		volumeList = VolumeList(token)
		# Header
		if args.verbose:
			yield ['ID', 'Name', 'Size', 'Bootable', 'Encrypted', 'Description', 'Metadata']
		else:
			yield ['ID', 'Name', 'Size', 'Bootable', 'Encrypted', 'Description']
		# Body
		for volume in volumeList:
			if args.verbose:
				yield [volume.volumeId, volume.name, volume.size, volume.bootable, volume.encrypted, volume.description, volume.metadata]
			else:
				yield [volume.volumeId, volume.name, volume.size, volume.bootable, volume.encrypted, volume.description]

	@classmethod
	@prettyPrint()
	def addVolume(cls, token, args):
		volumeList = VolumeList(token)
		volId = volumeList.add(
				args.size,
				name=args.name,
				description=args.description,
				source=args.source,
				snapshotId=args.snapshotId,
				imageRef=args.image_ref,
				bootable=args.bootable,
				)
		if not args.quiet:
			yield ['ID']
			yield [volId]

	@classmethod
	@prettyPrint()
	def deleteVolume(cls, token, args):
		volumeList = VolumeList(token)
		vol = volumeList[args.id or args.name]
		volumeList.delete(vol.volumeId)

class ImageCommand:
	@classmethod
	def configureParser(cls, subparser):
		listImages = subparser.add_parser('list-images', help='list saved images in current region')
		listImages.add_argument('-v', '--verbose', action='store_true', help='verbose output')
		listImages.add_argument('-b', '--visibility', choices=['public', 'private'], help='filter by visibility of the image')
		listImages.add_argument('-s', '--sort', help='sort by comma delimited field names',
		                        default='visibility,name')
		listImages.set_defaults(func=cls.listImages)

		deleteImage = subparser.add_parser('delete-image', help='delete image')
		deleteImage.add_argument('-v', '--verbose', action='store_true', help='verbose output')
		deleteImage.add_argument('images', type=str, nargs='+', metavar='IMAGES', help='image names')
		deleteImage.set_defaults(func=cls.deleteImage)

		showQuota = subparser.add_parser('show-quota', help='show quota')
		showQuota.set_defaults(func=cls.showQuota)

		setQuota = subparser.add_parser('set-quota', help='set quota')
		setQuota.add_argument('-s', '--size', type=int, help='(50 + 500*n) GB')
		setQuota.set_defaults(func=cls.setQuota)

	@classmethod
	@prettyPrint()
	def listImages(cls, token, args):
		images  = ImageList(token)
		def filterFn(i):
			if args.visibility:
				return args.visibility == i.visibility
			return True

		def sortKey(i):
			fieldNames = args.sort.split(',')
			return tuple(getattr(i, f, '') for f in fieldNames)

		# Header
		if args.verbose:
			yield ['ID', 'Name', 'MinDisk', 'MinRam', 'Status', 'CreatedAt', 'Visibility']
		else:
			yield ['Name', 'Status', 'CreatedAt', 'Visibility']
		# Body
		for i in sorted(filter(filterFn, images), key=sortKey):
			if args.verbose:
				yield [i.imageId, i.name, i.min_disk, i.min_ram, i.status, i.created_at, i.visibility]
			else:
				yield [i.name, i.status, i.created_at, i.visibility]

	@classmethod
	def deleteImage(cls, token, args):
		images = ImageList(token)
		vms = VMList(token)
		for name in args.images:
			vmid = vms.toVmid(name)
			if vmid is None:
				raise error.ImageNotFound(name)
			images.delete(name)

	@classmethod
	@prettyPrint()
	def showQuota(cls, token, args):
		quota = Quota(token)
		yield ['Region', 'Size']
		yield [quota.region, quota.size]

	@classmethod
	@prettyPrint()
	def setQuota(cls, token, args):
		quota = Quota(token)
		quota.set(args.size)

if __name__ == '__main__':
	exit(main())

