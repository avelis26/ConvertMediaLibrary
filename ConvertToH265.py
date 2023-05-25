#!/usr/bin/env python3
import argparse
import json
import logging
import sys
import os
import re
import subprocess
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Full path to video file to convert to h265.")
args = parser.parse_args()
parameters = json.load(open('parameters.json'))
opsLog = parameters['log_parent_path'] + parameters['log_filename']
logging.basicConfig(
	level=logging.DEBUG,
	format="%(asctime)s [%(levelname)s] %(message)s",
	handlers=[
		logging.FileHandler(opsLog),
		logging.StreamHandler(sys.stdout)
	]
)
base = os.path.splitext(args.input)[0]
outputFile = base + '.mkv'
#os.rename(my_file, base + '.mp4')
#cmd = 'ffmpeg -i ' + re.escape(args.input.strip()) + ' -c:v libx265 -vtag hvc1 ' + re.escape(outputFile)
logging.debug(outputFile)
#os.system(cmd)
#re.escape(args.input.strip())
subprocess.call([
	'ffmpeg',
	'-i',
	args.input.strip(),
	'-c:v',
	'libx265',
	'-vtag',
	'hvc1',
    '-y',
	outputFile
])
logging.info('Conversion complete.')
