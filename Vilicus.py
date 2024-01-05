#!/usr/bin/env python3
# Need to update logic for creating manifest file so multiple systems don't contend.
# Needs better error handling to ensure status file reverts to inactive.
# Consider adding parameter to select witch encoder library to use (libx265 vs hevc_nvenc).
# Starting from cron fails, fix implemented but not  tested yet.
# Consider adding parameter for ffmpeg codec.
import argparse
import decimal
import fcntl
import json
import logging
import os
import socket
import sys
import time
import ffmpeg

def load_parameters(param_file):
    try:
        with open(param_file) as file:
            parameters = json.load(file)
        return parameters
    except Exception as e:
        logging.error(f"Failed to load parameters: {e}")
        sys.exit(1)

def setup_logging(ops_log):
    try:
        class CustomFormatter(logging.Formatter):
            def format(self, record):
                if record.levelname == 'WARNING':
                    record.levelname = 'WARN'
                return super().format(record)
        formatter = CustomFormatter("%(asctime)s	[%(levelname)s]	%(message)s")
        file_handler = logging.FileHandler(ops_log)
        stream_handler = logging.StreamHandler(sys.stdout)
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[file_handler, stream_handler]
        )
    except Exception as e:
        logging.error(f"Failed to set up logging: {e}")
        sys.exit(1)

def create_videos_manifest(parameters, status_file_path, id):
    logging.info('Creating non-h265 videos manifest...')
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
                        file_path_base = os.path.basename(file_path)
                        logging.warning(f"Failed to probe file: {file_path_base}")
        video_set = set(video_list)
        logging.info('Total Non-h265 Videos: ' + str(len(video_set)))
        with open(videos_manifest_path, 'w') as file:
            for video in video_set:
                file.write(video + '\n')
        logging.info('Non-h265 videos manifest created.')
        return videos_manifest_path
    except Exception as e:
        write_status(status_file_path, id, "inactive")
        logging.error(f"Failed to create videos manifest: {e}")
        sys.exit(1)

def soft_exit(exit_file_path, status_file_path, id):
    if os.path.exists(exit_file_path):
        write_status(status_file_path, id, "inactive")
        logging.info('EXECUTION STOPPED BY USER')
        logging.info('******************************************************')
        with open(exit_file_path, 'r') as file:
            contents = file.read()
        os.remove(exit_file_path)
        if contents.strip() == "reboot":
            i = 0
            while check_active_status(status_file_path) == True:
                time.sleep(10)
                i += 1
                if i == 1080:
                    logging.error("check_active_status timed out after 3 hours!")
                    sys.exit(1)
            os.system("sudo reboot")
        else:
            sys.exit()

def write_status(status_file_path, hostname, status):
    try:
        if not os.path.exists(status_file_path):
            with open(status_file_path, "w") as status_file:
                status_data = {"hosts": [{"hostname": hostname, "status": status}]}
                json.dump(status_data, status_file, indent=4)
                status_file.write("\n")
                logging.info("Status file created.")
        else:
            with open(status_file_path, "r+") as status_file:
                fcntl.flock(status_file.fileno(), fcntl.LOCK_EX)
                try:
                    status_data = json.load(status_file)
                except json.JSONDecodeError:
                    status_data = {"hosts": []}
                for host in status_data["hosts"]:
                    if host["hostname"] == hostname:
                        host["status"] = status
                        break
                else:
                    status_data["hosts"].append({"hostname": hostname, "status": status})
                status_file.seek(0)
                json.dump(status_data, status_file, indent=4)
                status_file.write("\n")
                status_file.truncate()
                fcntl.flock(status_file.fileno(), fcntl.LOCK_UN)
                logging.info("Status file updated.")
    except Exception as e:
        logging.error(f"An error occurred while writing status: {str(e)}")
        sys.exit(1)

def check_active_status(status_file_path):
    try:
        with open(status_file_path, "r") as status_file:
            fcntl.flock(status_file.fileno(), fcntl.LOCK_EX)
            status_data = json.load(status_file)
            for host in status_data["hosts"]:
                if host["status"] == "ACTIVE":
                    fcntl.flock(status_file.fileno(), fcntl.LOCK_UN)
                    return True
            fcntl.flock(status_file.fileno(), fcntl.LOCK_UN)
            return False
    except Exception as e:
        logging.error(f"Failed to load status file: {e}")
        sys.exit(1)

def convert_to_h265(source_file_path, fail_file_path):
    global total_before_filesize
    global total_after_filesize
    try:
        start_time = time.time()
        file_path_with_mkv = os.path.splitext(source_file_path)[0] + '.mkv'
        file_name_with_mkv = os.path.basename(file_path_with_mkv)
        original_file_name = os.path.basename(source_file_path)
        old_file = source_file_path + '.old'
        old_file_base = os.path.basename(old_file)
        source_file_base = os.path.basename(source_file_path)
        logging.info('--------------------------------------------------------------------------------')
        logging.info(original_file_name)
        os.rename(source_file_path, old_file)
        ffmpeg.input(old_file).output(file_path_with_mkv, vcodec='hevc_nvenc', preset=18, qp=24).run()
        ffmpeg.input(file_path_with_mkv).output('pipe:', format='null', vframes=128).run()
        logging.info("Video validation succeeded.")
        before_file_size = os.path.getsize(old_file)
        after_file_size = os.path.getsize(file_path_with_mkv)
        difference = before_file_size - after_file_size
        total_before_filesize.append(before_file_size)
        total_after_filesize.append(after_file_size)
        total_difference = sum(total_before_filesize) - sum(total_after_filesize)
        space_saved = round((decimal.Decimal(total_difference) / decimal.Decimal(1073741824)), 2)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_time_formatted = time.strftime("%H:%M:%S", time.gmtime(execution_time))
        logging.info(f'Conversions:    {conversion_counter}')
        logging.debug(f'Before Size:    {before_file_size}')
        logging.debug(f'After Size:     {after_file_size}')
        logging.debug(f'Difference:     {difference}')
        logging.info(f'Difference MBs: {round((difference / (1024**2)), 2)}')
        logging.info(f"Execution Time: {execution_time_formatted}")
        logging.debug(f'Total Diff(B):  {total_difference}')
        logging.info(f'Total Diff(GB): {space_saved} GBs')
        os.remove(old_file)
    except ffmpeg.Error as e:
        logging.error(f"FFMPEG ERROR!!! {e}")
        if os.path.exists(file_path_with_mkv):
            os.remove(file_path_with_mkv)
            logging.info(f"Deleted {file_name_with_mkv}")
        
        if os.path.exists(old_file):
            logging.info(f"Rename OLD: {old_file_base}")
            logging.info(f"Rename NEW: {source_file_base}")
            os.rename(old_file, source_file_path)
        with open(fail_file_path, 'w') as file:
            file.write(source_file_path)
    except Exception as e:
        logging.error(f"Failed to convert file: {source_file_path}")
        logging.error(f"{str(e)}")
        if os.path.exists(file_path_with_mkv):
            os.remove(file_path_with_mkv)
            logging.info(f"Deleted {file_name_with_mkv}")
        if os.path.exists(old_file):
            logging.info(f"Rename OLD: {old_file_base}")
            logging.info(f"Rename NEW: {source_file_base}")
            os.rename(old_file, source_file_path)
        with open(fail_file_path, 'w') as file:
            file.write(source_file_path)

def write_ffmpeg_info():
    try:
        ffmpeg_version = ffmpeg.get_ffmpeg_version()
        ffmpeg_path = ffmpeg_version.get('ffmpeg_command', 'ffmpeg')
        logging.debug(f'FFmpeg Path: {ffmpeg_path}')
        cuda_info = ffmpeg_version.get('configuration', '').find('--enable-cuda') != -1
        if cuda_info:
            logging.debug('CUDA is enabled in FFmpeg configuration.')
        else:
            logging.debug('CUDA is not enabled in FFmpeg configuration.')
    except ffmpeg.Error as e:
        print(f'Error: {e}')

def main():
    global conversion_counter
    parser = argparse.ArgumentParser(description='Find and convert all non-h265 video files to h265 with ffmpeg.')
    parser.add_argument('-p', '--paramfile', type=str, help='Path to the input parameters file.', required=True)
    parser.add_argument('-s', '--skipManifest', action='store_true', default=False, help='Skip creating manifest.')
    args = parser.parse_args()
    parameters = load_parameters(args.paramfile)
    os.makedirs(parameters['log_parent_path'], exist_ok=True)
    ops_log = os.path.join(parameters['log_parent_path'], parameters['log_filename'])
    status_file_path = os.path.join(parameters['status_parent_path'], parameters['status_filename'])
    exit_file_path = os.path.join(parameters['log_parent_path'], parameters['exit_filename'])
    id = socket.gethostname() + '.' + parameters['manifest_filename']
    setup_logging(ops_log)
    logging.info('******************************************************')
    logging.info('EXECUTION START')
    logging.debug(f'input_path:           {parameters["videos_parent_path"]}')
    logging.debug(f'manifest_path:        {parameters["log_parent_path"]}')
    logging.debug(f'opsLog:               {ops_log}')
    logging.debug(f'exitFile:             {exit_file_path}')
    write_status(status_file_path, id, "ACTIVE")
    
    if args.skipManifest:
        logging.info('Skipping manifest creation.')
        videos_manifest_path = os.path.join(parameters['log_parent_path'], parameters['manifest_filename'])
    else:
        videos_manifest_path = create_videos_manifest(parameters, status_file_path, id)
    soft_exit(exit_file_path, status_file_path, id)
    logging.info('Beginning ffmpeg conversions...')
    with open(videos_manifest_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            conversion_counter += 1
            convert_to_h265(line.strip(), parameters['log_parent_path'] + parameters['fail_filename'])
            soft_exit(exit_file_path, status_file_path, id)
    write_status(status_file_path, id, "inactive")
    logging.info('EXECUTION STOP')
    logging.info('******************************************************')

if __name__ == "__main__":
    conversion_counter = 0
    total_before_filesize = []
    total_after_filesize = []
    main()
