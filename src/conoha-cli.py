#!/usr/bin/env python3
# -*- coding: utf8 -*-
from conoha.config import Config
from argparse import ArgumentParser

def main():
	parser = getArgumentParser()
	parser.parse_args()

def getArgumentParser():
	parser = ArgumentParser()
	subparser = parser.add_subparsers()
	subparser.required = True

	parser_compute = subparser.add_parser('compute')
	subparser_compute = parser_compute.add_subparsers()
	subparser_compute.required = True

	parser_compute_plans = subparser_compute.add_parser('plans')
	parser_compute_plans.add_argument('--ram', type=str)
	parser_compute_plans.add_argument('--cpu', type=int)
	parser_compute_plans.add_argument('--storage', type=str)

	parser_compute_list = subparser_compute.add_parser('list')
	parser_compute_list.add_argument('--name', type=str)
	parser_compute_list.add_argument('--region', type=str)
	parser_compute_list.add_argument('--status', type=str)
	parser_compute_list.add_argument('--plan', type=str)

	parser_compute_add = subparser_compute.add_parser('add')
	parser_compute_add.add_argument('--name', type=str)
	parser_compute_add.add_argument('--id', type=str)

	parser_compute_status = subparser_compute.add_parser('status')
	parser_compute_status.add_argument('--name', type=str)
	parser_compute_status.add_argument('--id', type=str)

	parser_compute_start = subparser_compute.add_parser('start')
	parser_compute_start.add_argument('--name', type=str)
	parser_compute_start.add_argument('--id', type=str)

	parser_compute_stop = subparser_compute.add_parser('stop')
	parser_compute_stop.add_argument('--name', type=str)
	parser_compute_stop.add_argument('--id', type=str)
	parser_compute_stop.add_argument('--force', type=str)

	parser_compute_reboot = subparser_compute.add_parser('reboot')
	parser_compute_reboot.add_argument('--name', type=str)
	parser_compute_reboot.add_argument('--id', type=str)
	parser_compute_reboot.add_argument('--force', type=str)

	parser_compute_delete = subparser_compute.add_parser('delete')
	parser_compute_delete.add_argument('--name', type=str)
	parser_compute_delete.add_argument('--id', type=str)
	parser_compute_delete.add_argument('--force', type=str)

	parser_compute_resize = subparser_compute.add_parser('resize')
	parser_compute_resize.add_argument('--name', type=str)
	parser_compute_resize.add_argument('--id', type=str)
	parser_compute_resize.add_argument('--plan', type=str)

	return parser

if __name__ == '__main__':
	exit(main())

