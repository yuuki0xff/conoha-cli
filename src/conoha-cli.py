#!/usr/bin/env python3
# -*- coding: utf8 -*-
from conoha.api import Token
from conoha.config import Config
from argparse import ArgumentParser
import sys
from conoha.compute import VMPlanList, VMImageList, VMList, KeyList

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
	token = Token(
			userName=conf['api']['user'],
			password=conf['api']['passwd'],
			tenantId=conf['api']['tenantId']
			)
	parsed_args.func(token, parsed_args)

def getArgumentParser():
	parser = ArgumentParser()
	subparser = parser.add_subparsers()

	parser_compute = subparser.add_parser('compute')
	subparser_compute = parser_compute.add_subparsers()
	ComputeCommand.configureParser(subparser_compute)

	return parser

class ComputeCommand():
	@classmethod
	def configureParser(cls, subparser):
		plans = subparser.add_parser('plans')
		plans.set_defaults(func=cls.plans)

		list_ = subparser.add_parser('list')
		list_.add_argument('--verbose', action='store_true')
		list_.add_argument('--vms', action='store_true')
		list_.add_argument('--images', action='store_true')
		list_.add_argument('--keys', action='store_true')
		list_.set_defaults(func=cls.list_)

		add = subparser.add_parser('add')
		add.add_argument('--quiet', action='store_true')
		add.add_argument('--name', type=str)
		add.add_argument('--imageid', type=str)
		add.add_argument('--planid', type=str)
		add.add_argument('--passwd', type=str)
		add.add_argument('--key', type=str)
		add.set_defaults(func=cls.add)

		status = subparser.add_parser('status')
		status.add_argument('--name', type=str)
		status.add_argument('--id', type=str)
		status.set_defaults(func=cls.status)

		start = subparser.add_parser('start')
		start.add_argument('--name', type=str)
		start.add_argument('--id', type=str)
		start.set_defaults(func=cls.start)

		stop = subparser.add_parser('stop')
		stop.add_argument('--name', type=str)
		stop.add_argument('--id', type=str)
		stop.add_argument('--force', action='store_true')
		stop.set_defaults(func=cls.stop)

		reboot = subparser.add_parser('reboot')
		reboot.add_argument('--name', type=str)
		reboot.add_argument('--id', type=str)
		reboot.set_defaults(func=cls.reboot)

		delete = subparser.add_parser('delete')
		delete.add_argument('--name', type=str)
		delete.add_argument('--id', type=str)
		delete.set_defaults(func=cls.delete)

		resize = subparser.add_parser('resize')
		resize.add_argument('--name', type=str)
		resize.add_argument('--id', type=str)
		resize.add_argument('--plan', type=str)
		resize.set_defaults(func=cls.resize)

	@classmethod
	def plans(cls, token, args):
		plans = VMPlanList(token)
		print(['ID', 'NAME', 'DISK', 'RAM', 'CPUs'])
		for p in plans:
			a = [p.planId, p.name, p.disk, p.ram, p.vcpus]
			print(a)

	@classmethod
	def list_(cls, token, args):
		if args.images:
			imageList = VMImageList(token)
			for img in imageList:
				if args.verbose:
					a = [img.imageId, img.name, img.minDisk, img.minRam, img.progress, img.status, img.created, img.updated]
				else:
					a = [img.imageId, img.name, img.status, img.created, img.updated]
				print(a)
		elif args.keys:
			keylist = KeyList(token)
			for key in keylist:
				if args.verbose:
					a = [key.name, key.publicKey, key.fingerprint]
				else:
					a = [key.name, key.fingerprint]
				print(a)
		else:
			vmlist = VMList(token)
			for vm in vmlist:
				if args.verbose:
					a = [vm.vmid, vm.flavorId, vm.hostId, vm.imageId, vm.tenantId, vm.name, vm.status, vm.created, vm.updated, vm.addressList, vm.securityGroupList]
				else:
					a = [vm.vmid, vm.name, vm.status]
				print(a)

	@classmethod
	def add(cls, token, args):
		vmlist = VMList(token)
		vmid = vmlist.add(args.imageid, args.planid, adminPass=args.passwd, keyName=args.key, name=args.name)
		if not args.quiet:
			print(vmid)

	@classmethod
	def status(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			a = [vm.vmid, vm.name, vm.status]
			print(['ID', 'NAME', 'STATUS'])
			print(a)

	@classmethod
	def start(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vm.start()

	@classmethod
	def stop(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vm.stop(args.force)

	@classmethod
	def reboot(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vm.restart()

	@classmethod
	def delete(cls, token, args):
		vmlist = VMList(token)
		vm = vmlist.getServer(vmid=args.id, name=args.name)
		if vm:
			vmlist.delete(vm.vmid)

	@classmethod
	def resize(cls, token, args): pass

if __name__ == '__main__':
	exit(main())

