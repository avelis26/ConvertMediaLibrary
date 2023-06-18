#!/usr/bin/env python3
import argparse
import decimal
import json
import logging
import os
import sys
import ffmpeg

def load_parameters(param_file):
    try:
        with open(param_file) as file:
            parameters = json.load(file)
        return parameters
    except Exception as e:
        logging.error(f"Failed to load parameters: {e}")
        raise SystemExit(1)

def setup_logging(ops_log):
    try:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(ops_log),
                logging.StreamHandler(sys.stdout)
            ]
        )
    except Exception as e:
        logging.error(f"Failed to set up logging: {e}")
        raise SystemExit(1)

def create_videos_manifest(parameters):
    try:
        input_path = parameters['videos_parent_path']
        videos_manifest_path = os.path.join(parameters['log_parent_path'], parameters['manifest_filename'])
        if os.path.exists(videos_manifest_path):
            os.remove(videos_manifest_path)
        video_list = []
        for current_path, _, file_names in os.walk(input_path):
            for file_name in file_names:
                file_path = os.path.join(current_path, file_name)
                file_size = os.path.getsize(file_path)
                if file_size > parameters['min_file_size']:
                    try:
                        probe_output = ffmpeg.probe(file_path)
                        for stream in probe_output['streams']:
                            if stream['codec_type'] == 'video' and stream['codec_name'] != 'hevc':
                                video_list.append(file_path)
                    except ffmpeg.Error as e:
                        logging.error(f"Failed to probe file: {file_path}")
        video_set = set(video_list)
        logging.info('Total Non-h265 Videos: ' + str(len(video_set)))
        with open(videos_manifest_path, 'w') as file:
            for video in video_set:
                file.write(video + '\n')
        logging.info('Non-h265 videos manifest created.')
        return videos_manifest_path
    except Exception as e:
        logging.error(f"Failed to create videos manifest: {e}")
        raise SystemExit(1)

def soft_exit(exit_file_path):
    if os.path.exists(exit_file_path):
        logging.info('EXECUTION STOPPED BY USER')
        logging.info('******************************************************')
        sys.exit()

def convert_to_h265(source_file_path):
    global total_before_filesize
    global total_after_filesize
    try:
        base = os.path.splitext(source_file_path)[0]
        output_file = base + '.mkv'
        logging.debug(output_file)
        os.rename(source_file_path, source_file_path + '.old')
        ffmpeg.input(source_file_path + '.old').output(output_file, vcodec="libx265", crf=28, acodec="copy", **{'threads:v': '1'}).run()
        ffmpeg.input(output_file).output("null", f="null").run()
        logging.info("Video validation succeeded.")
        before_file_size = os.path.getsize(source_file_path + '.old')
        after_file_size = os.path.getsize(output_file)
        difference = before_file_size - after_file_size
        total_before_filesize.append(before_file_size)
        total_after_filesize.append(after_file_size)
        total_difference = sum(total_before_filesize) - sum(total_after_filesize)
        space_saved = round((decimal.Decimal(total_difference) / decimal.Decimal(1073741824)), 2)
        logging.debug(f'Before Size:    {before_file_size}')
        logging.debug(f'After Size:     {after_file_size}')
        logging.debug(f'Difference:     {difference}')
        logging.info(f'Conversions:    {conversion_counter}')
        logging.debug(f'Total Diff(B):  {total_difference}')
        logging.info(f'Total Diff(GB): {space_saved} GBs')
        os.remove(source_file_path + '.old')
    except Exception as e:
        logging.error(f"Failed to convert file: {source_file_path}")
        logging.error(e)
        sys.exit(1)

def main():
    global conversion_counter
    parser = argparse.ArgumentParser(description='Find and convert all non-h265 video files to h265 with ffmpeg.')
    parser.add_argument('-p', '--paramfile', type=str, help='Path to the input parameters file', required=True)
    args = parser.parse_args()
    parameters = load_parameters(args.paramfile)
    os.makedirs(parameters['log_parent_path'], exist_ok=True)
    ops_log = os.path.join(parameters['log_parent_path'], parameters['log_filename'])
    exit_file_path = os.path.join(parameters['log_parent_path'], parameters['exit_filename'])
    setup_logging(ops_log)
    logging.info('******************************************************')
    logging.info('EXECUTION START')
    logging.debug(f'input_path:           {parameters["videos_parent_path"]}')
    logging.debug(f'manifest_path:        {parameters["log_parent_path"]}')
    logging.debug(f'opsLog:               {ops_log}')
    logging.debug(f'exitFile:             {exit_file_path}')
    logging.info('Creating non-h265 videos manifest...')
    videos_manifest_path = create_videos_manifest(parameters)
    soft_exit(exit_file_path)
    logging.info('Beginning ffmpeg conversions...')
    with open(videos_manifest_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            conversion_counter += 1
            convert_to_h265(line.strip())
            soft_exit(exit_file_path)
    logging.info('EXECUTION STOP')
    logging.info('******************************************************')

if __name__ == "__main__":
    conversion_counter = 0
    total_before_filesize = []
    total_after_filesize = []
    main()
