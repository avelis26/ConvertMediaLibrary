import os
import shutil
import subprocess
import argparse
import logging
import concurrent.futures

# Global variables to track conversion progress
total_saved_space = 0
completed_conversions = 0


def probe_video_encoding(file_path):
    # Execute FFmpeg command to probe video encoding
    command = ['ffmpeg', '-i', file_path]
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the output contains H.265/HEVC
    return 'hevc' in result.stdout.lower()


def convert_media_file(file_path, destination_dir):
    global total_saved_space, completed_conversions

    # Extract the file name and extension
    file_name = os.path.basename(file_path)
    file_base_name, file_ext = os.path.splitext(file_name)

    # Create the destination file path with H.265/HEVC encoding
    destination_file_path = os.path.join(destination_dir, f'{file_base_name}_hevc{file_ext}')

    # Execute FFmpeg command to convert the media file to H.265/HEVC
    command = ['ffmpeg', '-i', file_path, '-c:v', 'libx265', '-crf', '28', '-c:a', 'copy', destination_file_path]
    subprocess.run(command, check=True)

    # Calculate the saved space by comparing file sizes
    original_size = os.path.getsize(file_path)
    converted_size = os.path.getsize(destination_file_path)
    saved_space = original_size - converted_size

    # Update the global variables
    total_saved_space += saved_space
    completed_conversions += 1

    return destination_file_path


def convert_media_library(source_dir, destination_dir, log_file):
    global total_saved_space, completed_conversions

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Open the log file in append mode
    with open(log_file, 'a') as log:
        # Write initial progress to the log file
        log.write('Conversion Progress:\n')

        # Walk through the source directory and convert video files
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for root, _, files in os.walk(source_dir):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if os.path.isfile(file_path) and file_name.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                        if not probe_video_encoding(file_path):
                            future = executor.submit(convert_media_file, file_path, destination_dir)
                            futures.append(future)

            # Process the completed conversions and log progress
            for future in concurrent.futures.as_completed(futures):
                converted_file_path = future.result()
                if converted_file_path:
                    log.write(f'Converted: {converted_file_path}\n')

            # Log the total saved space and number of conversions
            log.write(f'Total Saved Space: {total_saved_space / (1024 * 1024)} MB\n')
            log.write(f'Completed Conversions: {completed_conversions}\n')


def main():
    parser = argparse.ArgumentParser(description='Media Library Conversion Tool')
    parser.add_argument('-s', '--source', help='Source directory', required=True)
    parser.add_argument('-d', '--destination', help='Destination directory', required=True)
    parser.add_argument('-l', '--log-file', help='Log file path', default='conversion.log')

    args = parser.parse_args()

    # Validate source directory
    if not os.path.isdir(args.source):
        logging.error('Source directory does not exist.')
        return

    # Convert the media library
    convert_media_library(args.source, args.destination, args.log_file)


if __name__ == '__main__':
    main()
