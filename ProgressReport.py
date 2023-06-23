#!/usr/bin/env python3
import argparse
import decimal
import json
import re

parser = argparse.ArgumentParser(description='Analyze log and report metrics.')
parser.add_argument('-p', '--paramfile', type=str, help='Path to the input parameters file', required=True)
args = parser.parse_args()
parameters = json.load(open(args.paramfile))
opsLog = parameters['log_parent_path'] + parameters['log_filename']

# Extract number from string and add to array.
total = []
patrn = "Difference:"
file = open(opsLog, "r")
for line in file:
	if re.search(patrn, line):
		list = line.split()
		num = int(list[-1])
		total.append(num)
		print(line)
space_saved = str(round((decimal.Decimal(sum(total)) / decimal.Decimal(1073741824)), 2))
print("Total Space Saved: " + space_saved + " GBs")
print("Total Conversions: " + str(len(total)))
file.close()