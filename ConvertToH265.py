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
time.sleep(64)
#inputFile = '/mnt/data/Media/Movies/Spies_Like_Us_\(1985\)/Spies_Like_Us_\(1985\).mp4'
#outputFile = '/mnt/data/Media/Movies/Spies_Like_Us_\(1985\)/test.mp4'
#cmd = 'ffmpeg -i ' + inputFile + ' -c:v libx265 -vtag hvc1 ' + outputFile
#os.system(cmd)
logging.info('Conversion complete.')
