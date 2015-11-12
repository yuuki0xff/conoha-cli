#!/usr/bin/env python3
# -*- coding: utf8 -*-
from conoha.config import Config
from argparse import ArgumentParser
import sys

def main():
	parser = getArgumentParser()
	try:
		parsed_args = parser.parse_args()
		# サブコマンドだけを指定した場合は失敗
		assert('func' in parsed_args)
		print(parsed_args)
	except AssertionError:
		# 失敗した場合は、そのサブコマンドに対応するhelpを表示
		parser.parse_args(sys.argv[1:]+['-h'])

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

		list_ = subparser.add_parser('list')
		list_.add_argument('--verbose', action='store_true')

		add = subparser.add_parser('add')
		add.add_argument('--quiet', action='store_true')
		add.add_argument('--name', type=str)
		add.add_argument('--passwd', type=str)
		add.add_argument('--key', type=str)

		status = subparser.add_parser('status')
		status.add_argument('--name', type=str)
		status.add_argument('--id', type=str)

		start = subparser.add_parser('start')
		start.add_argument('--name', type=str)
		start.add_argument('--id', type=str)

		stop = subparser.add_parser('stop')
		stop.add_argument('--name', type=str)
		stop.add_argument('--id', type=str)
		stop.add_argument('--force', action='store_true')

		reboot = subparser.add_parser('reboot')
		reboot.add_argument('--name', type=str)
		reboot.add_argument('--id', type=str)

		delete = subparser.add_parser('delete')
		delete.add_argument('--name', type=str)
		delete.add_argument('--id', type=str)

		resize = subparser.add_parser('resize')
		resize.add_argument('--name', type=str)
		resize.add_argument('--id', type=str)
		resize.add_argument('--plan', type=str)

if __name__ == '__main__':
	exit(main())

