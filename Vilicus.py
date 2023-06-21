#!/usr/bin/env python3
import argparse
import decimal
import json
import logging
import os
import sys
import time
import ffmpeg

start_time = time.time()

# PARAM
def load_parameters(param_file):
    try:
        with open(param_file) as file:
            parameters = json.load(file)
        return parameters
    except Exception as e:
        logging.info(get_run_time(start_time))
        logging.error(f"Failed to load parameters: {e}")
        sys.exit(1)

# LOG
def setup_logging(ops_log):
    try:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s	[%(levelname)s]	%(message)s",
            handlers=[
                logging.FileHandler(ops_log),
                logging.StreamHandler(sys.stdout)
            ]
        )
    except Exception as e:
        logging.info(get_run_time(start_time))
        logging.error(f"Failed to set up logging: {e}")
        sys.exit(1)

# CREATE
def create_status_file(status_file_path, server, workers):
    try:
        data = {
            workers: [
                {
                    "server_name": server,
                    "status": "idle",
                    "file": "none"
                }
            ]
        }
        with open(status_file_path, 'w') as status_file:
            json.dump(data, status_file, indent=4)
            status_file.write('\n')
    except Exception as e:
        logging.info(get_run_time(start_time))
        logging.error(f"Failed to create status file: {e}")
        sys.exit(1)

# UPDATE
def update_status_file(status_file_path, server, key, value, workers):
    try:
        with open(status_file_path, 'r') as status_file:
            data = json.load(status_file)
        for worker in data[workers]:
            if worker['server_name'] == server:
                worker[key] = value
                break
        with open(status_file_path, 'w') as status_file:
            json.dump(data, status_file, indent=4)
            status_file.write('\n')
    except Exception as e:
        logging.info(get_run_time(start_time))
        logging.error(f"Failed to update status file: {e}")
        sys.exit(1)

# ADD
def add_server_to_status_file(status_file_path, server, workers):
    try:
        with open(status_file_path, 'r') as status_file:
            data = json.load(status_file)
        new_server = {
            "server_name": server,
            "status": "idle",
            "file": "none"
        }
        data[workers].append(new_server)
        with open(status_file_path, 'w') as status_file:
            json.dump(data, status_file, indent=4)
            status_file.write('\n')
    except Exception as e:
        logging.info(get_run_time(start_time))
        logging.error(f"Failed to add {server} to status file: {e}")
        sys.exit(1)

# VERIFY
def verify_server_in_status_file(status_file_path, server, workers):
    try:
        check = False
        with open(status_file_path, 'r') as status_file:
            data = json.load(status_file)
        for worker in data[workers]:
            if worker['server_name'] == server:
                check = True
                break
        return check
    except Exception as e:
        logging.info(get_run_time(start_time))
        logging.error(f"Failed to verify status file: {e}")
        sys.exit(1)

# READ
def read_status_file(status_file_path):
    try:
        with open(status_file_path, 'r') as status_file:
            data = json.load(status_file)
        return data
    except Exception as e:
        logging.info(get_run_time(start_time))
        logging.error(f"Failed to read status file: {e}")
        sys.exit(1)

# PROBE
def probe_for_hevc(file_path):
    try:
        flag = False
        probe_output = ffmpeg.probe(file_path)
        for stream in probe_output['streams']:
            if stream['codec_type'] == 'video' and stream['codec_name'] != 'hevc':
                flag = True
    except ffmpeg.Error as e:
        logging.error(f"Failed to probe file: {file_path}")
    return flag

# MANIFEST
def create_videos_manifest(parameters):
    logging.info('Creating non-h265 videos manifest...')
    try:
        input_path = parameters['videos_parent_path']
        videos_manifest_path = os.path.join(parameters['videos_parent_path'], parameters['manifest_filename'])
        video_list = []
        for current_path, _, file_names in os.walk(input_path):
            for file_name in file_names:
                file_path = os.path.join(current_path, file_name)
                file_size = os.path.getsize(file_path)
                if file_size > parameters['min_file_size']:
                    if probe_for_hevc(file_path) == True:
                        video_list.append(file_path)           
        video_set = set(video_list)
        logging.info('Total Non-h265 Videos: ' + str(len(video_set)))
        with open(videos_manifest_path, 'w') as file:
            for video in video_set:
                file.write(video + '\n')
        logging.info('Non-h265 videos manifest created.')
        return videos_manifest_path
    except Exception as e:
        logging.info(get_run_time(start_time))
        logging.error(f"Failed to create videos manifest: {e}")
        sys.exit(1)

# EXIT
def soft_exit(exit_file_path, status_file_path, hostname, workers):
    if os.path.exists(exit_file_path):
        update_status_file(status_file_path, hostname, 'status', 'idle', workers)
        logging.info(get_run_time(start_time))
        logging.info('EXECUTION STOPPED BY USER')
        logging.info('******************************************************')
        sys.exit()

# TIME
def get_run_time(start_time):
    total_time = time.time() - start_time
    days, remainder = divmod(int(total_time), 86400)
    hours, remainder = divmod(int(remainder), 3600)
    minutes, seconds = divmod(int(remainder), 60)
    return (f"Total Run Time: {days} days {hours} hours {minutes} minutes {seconds} seconds")

# CONVERT
def convert_to_h265(source_file_path, fail_file_path, status_file_path, hostname, workers):
    global total_before_filesize
    global total_after_filesize
    update_status_file(status_file_path, hostname, 'file', source_file_path, workers)
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
    except Exception:
        logging.error(f"Failed to convert file: {source_file_path}")
        with open(fail_file_path, 'w') as file:
            file.write(source_file_path)

# MAIN
def main():
    global conversion_counter
    # Load parameters
    parser = argparse.ArgumentParser(description='Find and convert all non-h265 video files to h265 with ffmpeg.')
    parser.add_argument('-p', '--paramfile', type=str, help='Path to the input parameters file', required=True)
    args = parser.parse_args()
    parameters = load_parameters(args.paramfile)
    # Set arguments
    os.makedirs(parameters['log_parent_path'], exist_ok=True)
    ops_log = os.path.join(parameters['log_parent_path'], parameters['log_filename'])
    exit_file_path = os.path.join(parameters['log_parent_path'], parameters['exit_filename'])
    status_file_path = parameters['videos_parent_path'] + parameters['status_filename']
    videos_manifest_path = parameters['videos_parent_path'] + parameters['manifest_filename']
    hostname = os.uname().nodename
    workers = 'vilicus_workers'
    status_manifest_build = 'manifest'
    status_manifest_ready = 'ready'
    status_converting = 'converting'
    status_idle = 'idle'
    # Begin logging
    setup_logging(ops_log)
    logging.info('******************************************************')
    logging.info('EXECUTION START')
    logging.debug(f'host:                 {hostname}')
    logging.debug(f'input_path:           {parameters["videos_parent_path"]}')
    logging.debug(f'manifest_path:        {parameters["videos_parent_path"] + parameters["manifest_filename"]}')
    logging.debug(f'log_path:             {parameters["log_parent_path"]}')
    logging.debug(f'ops_log:              {ops_log}')
    logging.debug(f'fail_log:             {parameters["log_parent_path"] + parameters["fail_filename"]}')
    logging.debug(f'exitFile:             {exit_file_path}')
    # Create status file if not exists, and add current host if not exists
    if os.path.exists(status_file_path):
        logging.info(f'Status file found: {status_file_path}')
        if verify_server_in_status_file(status_file_path, hostname, workers) == False:
            logging.info('Adding server to status file...')
            add_server_to_status_file(status_file_path, hostname, workers)
    else:
        logging.info(f'Creating status file: {status_file_path}')
        create_status_file(status_file_path, hostname, workers)
    # If no servers converting or building manifist, create manifest
    status = read_status_file(status_file_path)
    check = False
    for worker in status[workers]:
        if worker['status'] == status_converting or worker['status'] == status_manifest_build or worker['status'] == status_manifest_ready:
            check = True
    if check == False:
        update_status_file(status_file_path, hostname, 'status', status_manifest_build, workers)
        if os.path.exists(videos_manifest_path):
            logging.info('Removing manifest...')
            os.remove(videos_manifest_path)
        create_videos_manifest(parameters)
        update_status_file(status_file_path, hostname, 'status', status_manifest_ready, workers)
    # If one server building manifest, wait for manifest
    status = read_status_file(status_file_path)
    check = False
    expire = 0
    for worker in status[workers]:
        if worker['status'] == status_manifest_build:
            check = True
            logging.info('Waiting for manifest...')
    while check == True:
        if expire > 720:
            logging.info(get_run_time(start_time))
            logging.error("Manifest build timed out!")
            sys.exit(1)
        time.sleep(5)
        status = read_status_file(status_file_path)
        count = 0
        for worker in status[workers]:
            if worker['status'] != status_manifest_build:
                count += 1
        if len(status[workers]) == count:
            check = False
        expire += 1
    # If one server converting or manifest ready, start converting
    status = read_status_file(status_file_path)
    check = False
    for worker in status[workers]:
        if worker['status'] == status_converting or worker['status'] == status_manifest_ready:
            check = True
    soft_exit(exit_file_path, status_file_path, hostname, workers)
    if check == True:
        logging.info('Beginning ffmpeg conversions...')
        update_status_file(status_file_path, hostname, 'status', status_converting, workers)
        with open(videos_manifest_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                status = read_status_file(status_file_path)
                count = 0
                for worker in status[workers]:
                    if worker['file'] == line:
                        count += 1
                if count == 0:
                    convert_to_h265(line.strip(), parameters['log_parent_path'] + parameters['fail_filename'], status_file_path, hostname, workers)
                    conversion_counter += 1
                soft_exit(exit_file_path, status_file_path, hostname, workers)
    else:
        logging.error("SOMETHING WENT WRONG")
    update_status_file(status_file_path, hostname, 'status', status_idle, workers)
    update_status_file(status_file_path, hostname, 'file', 'none', workers)
    logging.info(get_run_time(start_time))
    logging.info('EXECUTION STOP')
    logging.info('******************************************************')

if __name__ == "__main__":
    conversion_counter = 0
    total_before_filesize = []
    total_after_filesize = []
    main()
