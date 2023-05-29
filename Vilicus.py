#!/usr/bin/env python3
import json
import logging
import sys
import subprocess
import os
import ffmpeg

# Load parameters from json file and set vars.
try:
	parameters = json.load(open('parameters.json'))
	input_path = parameters['movies_parent_path']
	opsLog = parameters['log_parent_path'] + parameters['log_filename']
	movies_manifest_path = parameters['log_parent_path'] + parameters['movies_manifest_filename']
	exitFile = parameters['log_parent_path'] + parameters['exit_filename']
except Exception as e:
	print("ERROR01: ",e)
	exit()

# Create working directory ~/vilicus/ if not exist, delete manifest if exists.
try:
	if os.path.exists(parameters['log_parent_path']):
		if os.path.exists(movies_manifest_path):
			os.remove(movies_manifest_path)
	else:
		os.mkdir(parameters['log_parent_path'])
except Exception as e:
	print("ERROR02: ",e)
	exit()

# Set up logging to terminal and file.
try:
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
	logging.debug('input_path:           ' + input_path)
	logging.debug('movies_manifest_path: ' + movies_manifest_path)
	logging.debug('opsLog:               ' + opsLog)
	logging.debug('exitFile:             ' + exitFile)
	logging.info('Creating non-h265 movie manifest...')
except Exception as e:
	logging.error("ERROR03: " + str(e))
	exit()

# Define exit function to gracefully exit if exit file is found.
def softExit():
	if os.path.exists(exitFile):
		logging.info('EXECUTION STOPPED BY USER')
		logging.info('******************************************************')
		exit()

# Define function to rename source file, convert to h265, validate, delete source file.
def ConvertToH265(sourceFilePath):
	sourceFilePath = sourceFilePath.strip()
	base = os.path.splitext(sourceFilePath)[0]
	outputFile = base + '.mkv'
	logging.debug(outputFile)
	try:
		os.rename(sourceFilePath, sourceFilePath + '.old')
		subprocess.call([
			'ffmpeg',
			'-vaapi_device',
			'/dev/dri/renderD128',
			'-i',
			sourceFilePath + '.old',
			'-vf',
			'format=nv12,hwupload',
			'-c:v',
			'hevc_vaapi',
			'-vtag',
			'hvc1',
			outputFile
		])
	except Exception as e:
		logging.error("ERROR05: " + str(e))
		exit()
	try:
		(
			ffmpeg
			.input(outputFile)
			.output("null", f="null")
			.run()
		)
	except ffmpeg._run.Error as e:
		logging.error("ERROR06: " + str(e))
		exit()
	logging.info("Video validation succeeded.")
	try:
		os.remove(sourceFilePath + '.old')
	except Exception as e:
		logging.error("ERROR07: " + str(e))
		exit()
	logging.info('Conversion complete.')

# Create non-h265 movie manifest.
try:
	movie_list = []
	for current_path, directories, file_names in os.walk(input_path):
		for file_name in file_names:
			file_size = os.path.getsize(current_path + '/' + file_name)
			if file_size > parameters['min_file_size']:
				try:
					probe_output = ffmpeg.probe(current_path + '/' + file_name)
					for stream in probe_output['streams']:
						if (stream['codec_type'] == 'video'):
							if (stream['codec_name'] == 'hevc'):
								continue
							else:
								print(file_name)
								movie_list.append(current_path + '/' + file_name)
				except ffmpeg.Error as e:
					with open(opsLog, "a") as openFile:
						openFile.write(current_path + '/' + file_name + "\n")
					print(e.stderr)
	movie_set = set(movie_list)
	logging.info('Total Non-h265 Movies: ' + str(len(movie_set)))
	with open(movies_manifest_path, 'w') as openFile:
		for movie in movie_set:
			openFile.write("%s\n" % movie)
	logging.info('Non-h265 movie manifest created.')
except Exception as e:
	logging.error("ERROR04: " + str(e))
	exit()
softExit()

# Read manifest and convert 1 movie at a time.
logging.info('Beginning ffmpeg converstions...')
manifest_file = open(movies_manifest_path, 'r')
lines = manifest_file.readlines()
for line in lines:
	ConvertToH265(line)
	softExit()
logging.info('EXECUTION STOP')
logging.info('******************************************************')
