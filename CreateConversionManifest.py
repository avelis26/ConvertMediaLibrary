#!/usr/bin/env python3
import os
import ffmpeg
import json
from colorama import init, Fore, Back, Style
# Load parameters.json
parameters = json.load(open('parameters.json'))

input_path = '/mnt/data/Media/Movies/'
movies_manifest_path = '/mnt/data/Media/Movies/nonH265Roster.txt'
# h265_roster = '/mnt/data/Media/Movies/h265Roster.txt'
errorLog = '/mnt/data/Media/Movies/errorLog.txt'
os.system('clear')
# if os.path.exists(h265_roster):
# 	os.remove(h265_roster)
if os.path.exists(movies_manifest_path):
	os.remove(movies_manifest_path)
if os.path.exists(errorLog):
	os.remove(errorLog)
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
				with open(errorLog, "a") as openFile:
					openFile.write(current_path + '/' + file_name + "\n")
				print(e.stderr)