#!/usr/bin/env python3
import decimal
import re

# Extract number from string and add to array.
total = []
patrn = "Difference:"
file = open("/home/avelis/vilicus/vilicus.log", "r")
for line in file:
	if re.search(patrn, line):
		list = line.split()
		num = int(list[-1])
		total.append(num)
		print(line)
space_saved = decimal.Decimal(sum(total)) / decimal.Decimal(1073741824)
space_saved = str(round(space_saved, 2))
print("Total Space Saved: " + space_saved + " GBs")
file.close()