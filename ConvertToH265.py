#!/usr/bin/env python3
import argparse
import json
import logging
import sys
import time
import os
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

/mnt/data/Media/Movies/Back_To_The_Future_Part_II_(1989)/Back_To_The_Future_Part_II_(1989).mp4
outputFile = args.input
size = len(outputFile)
replacement = 'test.mkv'
outputFile = outputFile.replace(outputFile[size - 3:], replacement)
logging.debug(outputFile)
cmd = 'ffmpeg -i ' + args.input + ' -c:v libx265 -vtag hvc1 ' + outputFile
os.system(cmd)
logging.info('Conversion complete.')
