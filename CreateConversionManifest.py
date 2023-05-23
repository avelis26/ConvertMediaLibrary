#!/usr/bin/env python3
import os
import ffmpeg
import json
from colorama import init, Fore, Back, Style
# Load parameters.json
parameters = json.load(open('parameters.json'))
input_path = parameters['movies_parent_path']
movies_manifest_path = parameters['log_parent_path'] + '/' + parameters['movies_manifest_filename']
opsLog = parameters['log_parent_path'] + '/' + parameters['log_filename']
os.system('clear')
print('##### Parameters #####')
print('input_path: ' + input_path)
print('movies_manifest_path: ' + movies_manifest_path)
print('opsLog: ' + opsLog)
print('##### Parameters #####')
if os.path.exists(parameters['log_parent_path']):
	print('log_parent_path found')
if os.path.exists(movies_manifest_path):
	os.remove(movies_manifest_path)
if os.path.exists(opsLog):
	os.remove(opsLog)
for current_path, directories, file_names in os.walk(input_path):
	for file_name in file_names:
		file_size = os.path.getsize(current_path + '/' + file_name)
		if file_size > 268435456:
			print(Style.DIM + Fore.MAGENTA + current_path + '/' + file_name)
			try:
				probe_output = ffmpeg.probe(current_path + '/' + file_name)
				for stream in probe_output['streams']:
					if (stream['codec_type'] == 'video'):
						if (stream['codec_name'] == 'hevc'):
							print(Style.BRIGHT + Fore.GREEN + file_name)
							# with open(h265_roster, "a") as openFile:
							# 	openFile.write(current_path + '/' + file_name + "\n")
						else:
							print(Style.BRIGHT + Fore.YELLOW + file_name)
							with open(movies_manifest_path, "a") as openFile:
								openFile.write(current_path + '/' + file_name + "\n")
			except ffmpeg.Error as e:
				with open(opsLog, "a") as openFile:
					openFile.write(current_path + '/' + file_name + "\n")
				print(e.stderr)