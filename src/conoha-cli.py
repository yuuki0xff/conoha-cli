#!/usr/bin/env python3
# -*- coding: utf8 -*-
from conoha.api import Token
from conoha.config import Config
from argparse import ArgumentParser, FileType
import sys
from conoha.compute import VMPlanList, VMImageList, VMList, KeyList
from conoha.network import SecurityGroupList

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
		addKeyParser.add_argument('--file', type=FileType)
		addKeyParser.add_argument('--key', type=str)
		addKeyParser.set_defaults(func=cls.add_key)

		deleteKeyParser = subparser.add_parser('delete-key')
		deleteKeyParser.add_argument('--name', type=str)
		deleteKeyParser.set_defaults(func=cls.delete_key)

		addVmParser = subparser.add_parser('add-vm')
		addVmParser.add_argument('--quiet', action='store_true')
		addVmParser.add_argument('--name', type=str)
		addVmParser.add_argument('--imageid', type=str)
		addVmParser.add_argument('--planid', type=str)
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
	def list_plans(cls, token, args):
		plans = VMPlanList(token)
		print(['ID', 'NAME', 'DISK', 'RAM', 'CPUs'])
		for p in plans:
			a = [p.planId, p.name, p.disk, p.ram, p.vcpus]
			print(a)

	@classmethod
	def list_images(cls, token, args):
		imageList = VMImageList(token)
		for img in imageList:
			if args.verbose:
				a = [img.imageId, img.name, img.minDisk, img.minRam, img.progress, img.status, img.created, img.updated]
			else:
				a = [img.imageId, img.name, img.status, img.created, img.updated]
			print(a)

	@classmethod
	def list_keys(cls, token, args):
		keylist = KeyList(token)
		for key in keylist:
			if args.verbose:
				a = [key.name, key.publicKey, key.fingerprint]
			else:
				a = [key.name, key.fingerprint]
			print(a)

	@classmethod
	def list_vms(cls, token, args):
		vmlist = VMList(token)
		for vm in vmlist:
			if args.verbose:
				a = [vm.vmid, vm.flavorId, vm.hostId, vm.imageId, vm.tenantId, vm.name, vm.status, vm.created, vm.updated, vm.addressList, vm.securityGroupList]
			else:
				a = [vm.vmid, vm.name, vm.status]
			print(a)

	@classmethod
	def add_key(cls, token, args):
		keylist = KeyList(token)
		keylist.add(name=args.name, publicKey=args.key, publicKeyFile=args.file)

	@classmethod
	def delete_key(cls, token, args):
		keylist = KeyList(token)
		keylist.delete(args.name)

	@classmethod
	def add_vm(cls, token, args):
		groupNames = args.group_names and args.group_names.split(',')

		vmlist = VMList(token)
		vmid = vmlist.add(args.imageid, args.planid, adminPass=args.passwd, keyName=args.key, name=args.name, securityGroupNames=groupNames)
		if not args.quiet:
			print(vmid)

	@classmethod
	def start_vm(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vm.start()

	@classmethod
	def stop_vm(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vm.stop(args.force)

	@classmethod
	def reboot_vm(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vm.restart()

	@classmethod
	def delete_vm(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vmlist.delete(vm.vmid)

	@classmethod
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
		listRules.add_argument('--id', type=str)
		listRules.add_argument('--name', type=str)
		listRules.set_defaults(func=cls.listRules)

		addRule = subparser.add_parser('add-rule')
		addRule.add_argument('--id', type=str)
		addRule.add_argument('--direction', type=str)
		addRule.add_argument('--ethertype', type=str)
		addRule.add_argument('--port', type=str)
		addRule.add_argument('--protocol', type=str)
		addRule.add_argument('--remoteIPPrefix', type=str)
		addRule.set_defaults(func=cls.addRule)

		delRule = subparser.add_parser('delete-rule')
		delRule.add_argument('--group-id', type=str)
		delRule.add_argument('--rule-id', type=str)
		delRule.set_defaults(func=cls.deleteRule)

	@classmethod
	def listSecurityGroups(cls, token, args):
		sglist = SecurityGroupList(token)
		for sg in sglist:
			a = [sg.id_, sg.name, sg.description]
			print(a)

	@classmethod
	def addSecurityGroup(cls, token, args):
		sglist = SecurityGroupList(token)
		id_ = sglist.add(args.name, args.description)
		print(id_)

	@classmethod
	def deleteSecurityGroup(cls, token, args):
		sglist = SecurityGroupList(token)
		sg = sglist.getSecurityGroup(sgid=args.id, name=args.name)
		sglist.delete(sg.id_)

	@classmethod
	def listRules(cls, token, args):
		sglist = SecurityGroupList(token)
		sg = sglist.getSecurityGroup(sgid=args.id, name=args.name)

		for rule in sg.rules:
			if args.verbose:
				a = [rule.id_, rule.direction, rule.ethertype, rule.rangeMin, rule.rangeMax, rule.protocol, rule.remoteIPPrefix]
			else:
				a = [rule.direction, rule.ethertype, rule.rangeMin, rule.rangeMax, rule.protocol, rule.remoteIPPrefix]
			print(a)

	@classmethod
	def addRule(cls, token, args):
		sglist = SecurityGroupList(token)
		sg = sglist.getSecurityGroup(sgid=args.id)

		portMin = None
		portMax = None
		if args.port:
			if ',' in args.port:
				portMin, portMax = args.port.split(',')
			else:
				portMin = portMax = args.port

		sg.rules.add(args.direction, args.ethertype, portMin, portMax, args.protocol, args.remoteIPPrefix)

	@classmethod
	def deleteRule(cls, token, args):
		sglist = SecurityGroupList(token)
		sg = sglist.getSecurityGroup(sgid=args.group_id)
		sg.rules.delete(args.rule_id)

if __name__ == '__main__':
	exit(main())

