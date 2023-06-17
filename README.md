# ConvertMediaLibrary

Python scripts to automate converting all h264 videos to h265.

## Question Proposed To ChatGPT:
Please review and suggest improvements for the following python script:
```
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
```

## ChatGPT Summary
Here are some suggestions for improving the provided Python script:
1. Use a consistent indentation style: Python convention recommends using 4 spaces for indentation. Ensure that all indented blocks are consistently indented with 4 spaces for better readability.
2. Organize imports: It's a good practice to organize imports by grouping them into standard library imports, third-party library imports, and local imports. Import statements should be placed at the top of the script, immediately after the shebang line.
3. Use context managers for file handling: Instead of using json.load(open('parameters.json')), consider using the with statement to ensure proper file handling. For example, with open('parameters.json') as f: parameters = json.load(f). This will automatically close the file when done and handle any exceptions that might occur during file operations.
4. Avoid using global variables: It's generally recommended to avoid using global variables whenever possible. Instead, pass variables as function arguments and return values. This helps encapsulate functionality and makes the code easier to understand and maintain.
5. Provide meaningful error messages: When catching exceptions, it's helpful to provide more specific error messages that indicate the cause of the error. For example, instead of printing "ERROR01" or "ERROR02", provide a descriptive message that explains the issue encountered.
6. Use logging consistently: Make sure to use logging consistently throughout the script for all relevant log messages. Avoid mixing print statements with logging. If you're using logging for most of the script, it's better to use logging exclusively.
7. Handle exceptions gracefully: When encountering an exception, it's generally better to log the error and handle it gracefully rather than using exit(). Exiting abruptly may leave resources unclosed and prevent proper cleanup. Consider logging the error, providing an appropriate message, and allowing the script to continue or exit gracefully.
8. Encapsulate functionality in functions: Break down the script into smaller, reusable functions. This will improve code modularity, readability, and reusability. Each function should have a single responsibility, making the code easier to understand and maintain.
9. Add docstrings and comments: Add descriptive docstrings to functions and comments where necessary to explain the purpose and behavior of the code. This will help other developers (including your future self) understand the script more easily.
10. Consider using command-line arguments: Instead of hardcoding the paths and filenames in the script, you could consider using command-line arguments. This would make the script more flexible and allow users to specify the required paths and filenames when executing the script.
11. Consider using a configuration file or environment variables: Instead of hardcoding configuration values directly in the script, you might want to consider using a separate configuration file (e.g., JSON, YAML) or environment variables. This makes it easier to modify the script's behavior without modifying the code itself.

Please make sure to replace /path/to/log_directory/ with the actual path to your desired log directory. Additionally, verify and adjust any other paths and filenames according to your needs.

Remember to test the updated script with your specific use case and ensure it behaves as expected.

### Author
- [Graham Pinkston](https://github.com/avelis26)
- [Ai Used To Write This Code](https://chat.openai.com/)
