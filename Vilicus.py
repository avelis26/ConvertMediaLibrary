#!/usr/bin/env python3
import json
import logging
import sys
import time
import os
import ffmpeg
import decimal
total_before_filesize = []
total_after_filesize = []
conversion_counter = 0

def main():
	global conversion_counter
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
								if (stream['codec_name'] != 'hevc'):
									print(file_name)
									movie_list.append(current_path + '/' + file_name)
					except ffmpeg.Error as e:
						logging.error("ERROR06: " + (current_path + '/' + file_name))
						print(e.stderr)
		movie_set = set(movie_list)
		logging.info('Total Non-h265 Movies: ' + str(len(movie_set)))
		with open(movies_manifest_path, 'w') as openFile:
			for movie in movie_set:
				openFile.write("%s\n" % movie)
		logging.info('Non-h265 movie manifest created.')
	except Exception as e:
		logging.error("ERROR06: " + str(e))
		exit()
	softExit(exitFile)
	# Read manifest and convert 1 movie at a time.
	logging.info('Beginning ffmpeg converstions...')
	manifest_file = open(movies_manifest_path, 'r')
	lines = manifest_file.readlines()
	for line in lines:
		conversion_counter += 1
		ConvertToH265(line)
		softExit(exitFile)
	logging.info('EXECUTION STOP')
	logging.info('******************************************************')

# Define exit function to gracefully exit if exit file is found.
def softExit(exitFilePath):
	if os.path.exists(exitFilePath):
		logging.info('EXECUTION STOPPED BY USER')
		logging.info('******************************************************')
		exit()

# Define function to rename source file, convert to h265, validate, delete source file.
def ConvertToH265(sourceFilePath):
	global conversion_counter
	global total_before_filesize
	global total_after_filesize
	sourceFilePath = sourceFilePath.strip()
	base = os.path.splitext(sourceFilePath)[0]
	outputFile = base + '.mkv'
	logging.debug(outputFile)
	try:
		os.rename(sourceFilePath, sourceFilePath + '.old')
		ffmpeg.input(sourceFilePath + '.old').output(outputFile, vcodec="libx265", crf=28, acodec="copy").run()
		time.sleep(2)
		ffmpeg.input(outputFile).output("null", f="null").run()
		logging.info("Video validation succeeded.")
	except Exception as e:
		logging.error("ERROR04: " + str(e))
		exit()
	try:
		before_file_size = os.path.getsize(sourceFilePath + '.old')
		after_file_size = os.path.getsize(outputFile)
		total_before_filesize.append(before_file_size)
		total_after_filesize.append(after_file_size)
		total_difference = sum(total_before_filesize) - sum(total_after_filesize)
		space_saved = decimal.Decimal(total_difference) / decimal.Decimal(1073741824)
		space_saved = round(space_saved, 2)
		logging.debug('Before Size: ' + str(before_file_size))
		logging.debug('After Size:  ' + str(after_file_size))
		logging.debug('Difference:  ' + str(before_file_size - after_file_size))
		os.remove(sourceFilePath + '.old')
	except Exception as e:
		logging.error("ERROR05: " + str(e))
		exit()
	logging.info('Conversions complete: ' + str(conversion_counter))
	logging.debug('Total Diff:  ' + str(total_difference))
	logging.info('Gigabytes saved: ' + str(space_saved) + ' GBs')

if __name__ == "__main__":
	main()
