#!/usr/bin/env python3
import argparse
import json
import logging
import sys
import os
import re
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
logging.info('Converting ' + args.input + 'to h265...')
outputFile = args.input
size = len(outputFile)
replacement = 'mkv'
outputFile = outputFile.replace(outputFile[size - 3:], replacement)
logging.debug(outputFile)
cmd = 'ffmpeg -i ' + re.escape(args.input) + ' -c:v libx265 -vtag hvc1 ' + re.escape(outputFile)
logging.debug(cmd)
os.system(cmd)
logging.info('Conversion complete.')
