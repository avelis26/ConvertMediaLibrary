#!/usr/bin/env python3
import os
import ffmpeg
import json
import logging
import sys
from colorama import init, Fore, Back, Style
from shutil import rmtree
parameters = json.load(open('parameters.json'))
input_path = parameters['movies_parent_path']
movies_manifest_path = parameters['log_parent_path'] + parameters['movies_manifest_filename']
opsLog = parameters['log_parent_path'] + parameters['log_filename']
if os.path.exists(parameters['log_parent_path']):
	if os.path.exists(movies_manifest_path):
		os.remove(movies_manifest_path)
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
logging.debug('input_path:           ' + input_path)
logging.debug('movies_manifest_path: ' + movies_manifest_path)
logging.debug('opsLog:               ' + opsLog)
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
