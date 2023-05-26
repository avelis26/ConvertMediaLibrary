#!/usr/bin/env python3
import argparse
import json
import logging
import sys
import os
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
outputFile = base + '.mkv'
logging.debug(outputFile)
try:
	os.rename(args.input.strip(), args.input.strip() + '.old')
	subprocess.call([
		'ffmpeg',
		'-i',
		args.input.strip() + '.old',
		'-c:v',
		'libx265',
		'-vtag',
		'hvc1',
		outputFile
	])
except:
	logging.error("H265 conversion failed!!!")
	exit()
try:
	(
		ffmpeg
		.input(outputFile)
		.output("null", f="null")
		.run()
	)
except ffmpeg._run.Error:
	logging.error("Corrupt video!!!")
	exit()
logging.info("Video validation succeeded.")
try:
	os.remove(args.input.strip() + '.old')
except:
	logging.error("Failed to remove source video!!!")
	exit()
logging.info('Conversion complete.')
