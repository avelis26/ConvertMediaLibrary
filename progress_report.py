#!/usr/bin/env python3
import argparse
import decimal
import json
import re

parser = argparse.ArgumentParser(description='Analyze log and report metrics.')
parser.add_argument('-p', '--paramfile', nargs='+', help='Path to the input parameters file', required=True)
args = parser.parse_args()
total_conversions = []
total_space_saved = []
for paramfile in args.paramfile:
	parameters = json.load(open(paramfile))
	opsLog = parameters['log_parent_path'] + parameters['log_filename']
	total = []
	patrn = "Difference:"
	file = open(opsLog, "r")
	for line in file:
		if re.search(patrn, line):
			list = line.split()
			num = int(list[-1])
			total.append(num)
	space_saved = round((decimal.Decimal(sum(total)) / decimal.Decimal(1073741824)), 2)
	total_space_saved.append(space_saved)
	total_conversions.append(len(total))
	print(f"-{paramfile}")
	print(f"--Space Saved: {space_saved} GBs")
	print(f"--Conversions: {len(total)}")
	print("-")
	file.close()
print(f"Total Space Saved: {str(sum(total_space_saved))} GBs")
print(f"Total Conversions: {str(sum(total_conversions))}")

