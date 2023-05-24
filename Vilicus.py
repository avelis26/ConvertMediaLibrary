#!/usr/bin/env python3
import json
import logging
import sys
import time
import subprocess
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
logging.info('EXECUTION START')
logging.info('Creating non-h265 movie manifest...')
subprocess.run(["python3", "CreateConversionManifest.py"])
logging.info('Non-h265 movie manifest created.')
logging.info('Beginning ffmpeg converstion...')
subprocess.run(["python3", "test.py"])
logging.info('EXECUTION STOP')
logging.info('******************************************************')