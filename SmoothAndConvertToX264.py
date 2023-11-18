#!/usr/bin/env python3

import os
import subprocess
import time
from datetime import datetime


def execute_ffmpeg(input_file, output_file, log_file, codec, preset, bitrate):
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
            log.write(f"FFmpeg process PID: {ffmpeg_process.pid}\n")

    except subprocess.CalledProcessError as e:
        error_message = f"Error: {e}"
        print(error_message)
        with open(log_file, 'a') as log:
            log.write(error_message + '\n')


def execute_monitor(log_file, ffmpeg_pid):
    try:
        bash_script_template = """
log_file="{log_file}"
while kill -0 {ffmpeg_pid} 2>/dev/null; do
    sleep 1
done
echo "The FFmpeg process with PID {ffmpeg_pid} has completed." >> "$log_file"
start_time_string=$(head -n 1 "$log_file" | cut -d ' ' -f 4-)
start_time=$(date -d "$start_time_string" "+%s")
end_time=$(date "+%Y-%m-%d %H:%M:%S")
end_time_stamp=$(date -d "$end_time" "+%s")
execution_time=$((end_time_stamp - start_time))
hours=$((execution_time / 3600))
minutes=$(( (execution_time % 3600) / 60 ))
seconds=$((execution_time % 60))
echo "Script end time: $end_time" >> "$log_file"
echo "Execution time: $hours hours $minutes minutes $seconds seconds" >> "$log_file"
"""

        bash_script = bash_script_template.format(
            log_file=log_file, ffmpeg_pid=ffmpeg_pid)
        with open(log_file, 'a') as log:
            process = subprocess.Popen([
                'bash', '-c', bash_script
            ], stdout=log, stderr=subprocess.STDOUT)

    except subprocess.CalledProcessError as e:
        error_message = f"Error: {e}"
        print(error_message)
        with open(log_file, 'a') as log:
            log.write(error_message + '\n')


if __name__ == "__main__":
    try:
        os.system('clear')
        codec = 'h264_nvenc'
        preset = 'p7'
        bitrate = '14.4M'
        input_file = "/mnt/data/2023-11-13_18-48-32_Mugello_Race.mkv"
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"/mnt/data/{file_name}_{codec}_{preset}_{bitrate}.mp4"
        log_file = f"/mnt/data/ff_{file_name}_{codec}_{preset}_{bitrate}.log"
        start_time = time.time()
        start_datetime = datetime.fromtimestamp(start_time)
        with open(log_file, 'w') as log:
            log.write(
                f"Script start time: {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n")

        execute_ffmpeg(input_file, output_file,
                       log_file, codec, preset, bitrate)

        with open(log_file, 'r') as log:
            lines = log.readlines()
            ffmpeg_pid = None
            for line in reversed(lines):
                if "FFmpeg process PID:" in line:
                    ffmpeg_pid = int(line.split(":")[1].strip())
                    break

        execute_monitor(log_file, ffmpeg_pid)

    except Exception as e:
        error_message = f"Error: {e}"
        print(error_message)
        with open(log_file, 'a') as log:
            log.write(error_message + '\n')
