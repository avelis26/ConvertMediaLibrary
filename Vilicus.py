#!/usr/bin/env python3
import json
import logging
import sys
import subprocess
import os
parameters = json.load(open('parameters.json'))
opsLog = parameters['log_parent_path'] + parameters['log_filename']
movies_manifest_path = parameters['log_parent_path'] + parameters['movies_manifest_filename']
if os.path.exists(parameters['log_parent_path']):
	if os.path.exists(movies_manifest_path):
		os.remove(movies_manifest_path)
		print('remove me')
else:
	os.mkdir(parameters['log_parent_path'])
logging.basicConfig(
	level=logging.DEBUG,
	format="%(asctime)s [%(levelname)s] %(message)s",
	handlers=[
		logging.FileHandler(opsLog),
		logging.StreamHandler(sys.stdout)
	]
)
logging.info('******************************************************')
logging.info('EXECUTION START')
logging.info('Creating non-h265 movie manifest...')
subprocess.run(["python3", "CreateConversionManifest.py"])
logging.info('Non-h265 movie manifest created.')
logging.info('Beginning ffmpeg converstions...')
manifest_file = open(movies_manifest_path, 'r')
lines = manifest_file.readlines()
for line in lines:
	subprocess.run(["python3", "ConvertToH265.py", line])
logging.info('EXECUTION STOP')
logging.info('******************************************************')

#268435456