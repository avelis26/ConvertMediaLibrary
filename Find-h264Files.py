#!/usr/bin/env python3
import os
import sys
import json

inputPath = '/mnt/data/Media/Movies/'

codec = 'h264'
type = 'video'

cmd = 'ffprobe -v quiet -show_streams -print_format json ' + inputPath
output = os.popen(cmd).read()
output = json.loads(output)

for stream in output['streams']:
	if stream['codec_name'] == codec and stream['codec_type'] == type:
		print(inputPath)
		sys.exit(0)
