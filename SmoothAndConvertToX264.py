#!/usr/bin/env python3

import os
import subprocess
import time
from threading import Thread


def clear_screen():
    os.system('clear')


def run_finally_block(log_file, start_time):
    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_time_formatted = time.strftime(
        "%H hours : %M minutes : %S seconds", time.gmtime(execution_time_seconds))

    with open(log_file, 'a') as log:
        log.write(f"Script end time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Total execution time: {execution_time_formatted}\n")


def monitor_ffmpeg_completion(ffmpeg_process, log_file, start_time):
    ffmpeg_process.wait()
    run_finally_block(log_file, start_time)


def ff_convert_smooth(input_file, output_file, log_file, codec, preset, bitrate):
    try:
        with open(log_file, 'a') as log:
            ffmpeg_process = subprocess.Popen([
                '/usr/local/bin/ffmpeg',
                '-y',
                '-i', input_file,
                '-vf', "minterpolate='mi_mode=dup:mc_mode=aobmc:vsbmc=1'",
                '-c:v', codec,
                '-preset', preset,
                '-b:v', bitrate,
                output_file
            ], stdout=log, stderr=subprocess.STDOUT)

        monitor_thread = Thread(target=monitor_ffmpeg_completion, args=(
            ffmpeg_process, log_file, time.time()))
        monitor_thread.daemon = True  # Set the thread as daemon
        monitor_thread.start()

    except subprocess.CalledProcessError as e:
        error_message = f"Error: {e}"
        print(error_message)
        with open(log_file, 'a') as log:
            log.write(error_message + '\n')


if __name__ == "__main__":
    try:
        clear_screen()
        codec = 'h264_nvenc'
        preset = 'p7'
        bitrate = '14.4M'
        input_file = "/mnt/data/2023-11-13_16-20-20_Mugello_Qual.mkv"
        output_file = f"/mnt/data/output_{codec}_{preset}_{bitrate}.mp4"
        log_file = f"/mnt/data/ff_{codec}_{preset}_{bitrate}.log"
        with open(log_file, 'w') as log:
            log.write(
                f"Script start time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        ff_convert_smooth(input_file, output_file,
                          log_file, codec, preset, bitrate)

    except Exception as e:
        error_message = f"Error: {e}"
        print(error_message)
        with open(log_file, 'a') as log:
            log.write(error_message + '\n')
