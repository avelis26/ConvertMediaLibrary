#!/usr/bin/env python3
import argparse
import json
import logging
import sys
import os
#import re
import subprocess
import ffmpeg
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
outputFile = base + '.gp26'
logging.debug(outputFile)
#re.escape(args.input.strip())
try:
	subprocess.call([
		'ffmpeg',
		'-i',
		args.input.strip(),
		'-c:v',
		'libx265',
		'-vtag',
		'hvc1',
		outputFile
	])
except:
	logging.error("H265 conversion failed!!!")
try:
	(
		ffmpeg
		.input(outputFile)
		.output("null", f="null")
		.run()
	)
except ffmpeg._run.Error:
	logging.error("Corrupt video!!!")
else:
	logging.info("Video validation succeeded.")
os.remove(args.input)
os.rename(outputFile, base + '.mkv')
logging.info('Conversion complete.')
