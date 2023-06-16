import os
import shutil
import subprocess
import argparse
import logging
from multiprocessing import Pool


def probe_video_encoding(file_path):
    # Execute FFmpeg command to probe video encoding
    command = ['ffmpeg', '-i', file_path]
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the output contains H.265/HEVC
    return 'hevc' in result.stdout.lower()


def convert_media_file(file_path, destination_dir, conversion_options):
    # Check video encoding using FFmpeg probing
    is_hevc = probe_video_encoding(file_path)

    if is_hevc:
        # File is already encoded with H.265/HEVC, no conversion needed
        logging.info(f'Skipping conversion for {file_path}')
        return None

    # Extract the file name and extension
    file_name = os.path.basename(file_path)
    file_base_name, _ = os.path.splitext(file_name)

    # Create the destination file path with the desired format
    destination_file_path = os.path.join(destination_dir, file_base_name + conversion_options['output_format'])

    # Execute FFmpeg command to convert the media file
    command = ['ffmpeg', '-i', file_path] + conversion_options['extra_args'] + [destination_file_path]
    subprocess.run(command, check=True)

    return destination_file_path


def convert_media_library(source_dir, destination_dir, conversion_options):
    # Create a temporary directory to store the converted files
    temp_dir = os.path.join(destination_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    # Walk through the source directory and convert media files
    files_to_convert = []
    for root, _, files in os.walk(source_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                if probe_video_encoding(file_path):
                    files_to_convert.append(file_path)

    # Use multiprocessing to convert files concurrently
    with Pool() as pool:
        converted_files = pool.starmap(convert_media_file, [(file_path, temp_dir, conversion_options) for file_path in files_to_convert])

    # Move the converted files from the temporary directory to the destination directory
    for converted_file in converted_files:
        if converted_file:
            destination_path = os.path.join(destination_dir, os.path.basename(converted_file))
            shutil.move(converted_file, destination_path)

    # Remove the temporary directory
    shutil.rmtree(temp_dir)


def main():
    parser = argparse.ArgumentParser(description='Media Library Conversion Tool')
    parser.add_argument('-s', '--source', help='Source directory', required=True)
    parser.add_argument('-d', '--destination', help='Destination directory', required=True)
    parser.add_argument('-f', '--format', help='Output format (e.g., .mp4, .mkv)', default='.mp4')
    parser.add_argument('-a', '--extra-args', help='Additional FFmpeg arguments', default='', nargs='+')

    args = parser.parse_args()

    # Validate source and destination directories
    if not os.path.isdir(args.source):
        logging.error('Source directory does not exist.')
        return
    if not os.path.isdir(args.destination):
        logging.error('Destination directory does not exist.')
        return

    # Prepare conversion options
    conversion_options = {
        'output_format': args.format,
        'extra_args': args.extra_args
    }

    # Convert the media library
    convert_media_library(args.source, args.destination, conversion_options)


if __name__ == '__main__':
    main()
