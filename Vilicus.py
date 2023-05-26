#!/usr/bin/env python3
import json
import logging
import sys
import subprocess
import os
import ffmpeg
import argparse

# Load parameters from json file and set vars.
parameters = json.load(open('parameters.json'))
input_path = parameters['movies_parent_path']
opsLog = parameters['log_parent_path'] + parameters['log_filename']
movies_manifest_path = parameters['log_parent_path'] + parameters['movies_manifest_filename']

# Create working directory ~/vilicus/ if not exist, delete manifest if exists.
if os.path.exists(parameters['log_parent_path']):
	if os.path.exists(movies_manifest_path):
		os.remove(movies_manifest_path)
else:
	os.mkdir(parameters['log_parent_path'])

# Set up logging to terminal and file.
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
logging.info('Creating non-h265 movie manifest...')

# Create non-h265 movie manifest.
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

# Define function to rename source file, convert to h265, validate, delete source file.
def ConvertToH265(sourceFilePath):
	parser = argparse.ArgumentParser()
	parser.add_argument("input", help="Full path to video file to convert to h265.")
	args = parser.parse_args()
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







# Read manifest and convert 1 movie at a time.
logging.info('Beginning ffmpeg converstions...')
manifest_file = open(movies_manifest_path, 'r')
lines = manifest_file.readlines()
for line in lines:
	subprocess.run(["python3", "ConvertToH265.py", line])
logging.info('EXECUTION STOP')
logging.info('******************************************************')
