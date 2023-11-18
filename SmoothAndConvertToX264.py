#!/usr/bin/env python3

import os
import subprocess
import time


def clear_screen():
    os.system('clear')


def ff_convert_smooth(input_file, output_file, log_file):
    try:
        with open(log_file, 'a') as log:
            subprocess.Popen([
                '/usr/local/bin/ffmpeg',
                '-y',
                '-i', input_file,
                '-vf', "minterpolate='mi_mode=dup:mc_mode=aobmc:vsbmc=1'",
                '-c:v', 'hevc_nvenc',
                '-preset', 'p7',
                '-b:v', '14.4M',
                # '-c:a', 'aac',
                # '-b:a', '192k',
                output_file
            ], stdout=log, stderr=subprocess.STDOUT)

    except subprocess.CalledProcessError as e:
        error_message = f"Error: {e}"
        print(error_message)
        with open(log_file, 'a') as log:
            log.write(error_message + '\n')


if __name__ == "__main__":
    try:
        clear_screen()
        input_file = "/mnt/data/2023-11-13_16-20-20_Mugello_Qual.mkv"
        output_file = "/mnt/data/output_hevc_nvenc_p7_14.4M.mp4"
        log_file = "/mnt/data/ff_hevc_nvenc_p7_14.4M.log"
        start_time = time.time()
        with open(log_file, 'w') as log:
            log.write(f"Script start time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        ff_convert_smooth(input_file, output_file, log_file)

    except Exception as e:
        error_message = f"Error: {e}"
        print(error_message)
        with open(log_file, 'a') as log:
            log.write(error_message + '\n')

    finally:
        end_time = time.time()
        execution_time_seconds = end_time - start_time
        execution_time_formatted = time.strftime(
            "%H hours : %M minutes : %S seconds", time.gmtime(execution_time_seconds))

        with open(log_file, 'a') as log:
            log.write(f"Script end time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write(f"Total execution time: {execution_time_formatted}\n")