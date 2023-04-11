#!/usr/bin/env python3
import os
import ffmpeg
input_path = '/mnt/data/Media/Movies/'
non_h265_roster = '/mnt/data/Media/Movies/nonH265Roster.txt'
h265_roster = '/mnt/data/Media/Movies/h265Roster.txt'
os.system('clear')
if os.path.exists(h265_roster):
	os.remove(h265_roster)
if os.path.exists(non_h265_roster):
	os.remove(non_h265_roster)
for current_path, directories, file_names in os.walk(input_path):
	for file_name in file_names:
		file_size = os.path.getsize(current_path + '/' + file_name)
		if file_size > 268435456:
			probe_output = ffmpeg.probe(current_path + '/' + file_name)
			for stream in probe_output['streams']:
				if (stream['codec_type'] == 'video'):
					if (stream['codec_name'] == 'hevc'):
						with open(h265_roster, "a") as openFile:
							openFile.write(current_path + '/' + file_name + "\n")
					else:
						with open(non_h265_roster, "a") as openFile:
							openFile.write(current_path + '/' + file_name + "\n")
print('---1---')
os.system('cat ' + non_h265_roster)
print('---2---')
os.system('cat ' + h265_roster)