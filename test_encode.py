#!/usr/bin/env python3
import os
import ffmpeg
import time

def get_file_size(file_path):
    return os.path.getsize(file_path)

def convert_to_x265(input_file, output_file):
    start_time = time.time()
    input_size = get_file_size(input_file)
    (
        ffmpeg
        .input(input_file)
        .output(output_file, vcodec='hevc_nvenc', preset='slow', global_quality=23, c='copy')
        .run()
    )
    output_size = get_file_size(output_file)
    size_difference = (input_size - output_size) / (1024 * 1024)
    end_time = time.time()
    execution_time = end_time - start_time
    execution_time_formatted = time.strftime("%H:%M:%S", time.gmtime(execution_time))
    print(f"Input File Size: {input_size / (1024 * 1024):.2f} MB")
    print(f"Output File Size: {output_size / (1024 * 1024):.2f} MB")
    print(f"Size Difference: {size_difference:.2f} MB")
    print(f"Execution Time: {execution_time_formatted}")

if __name__ == "__main__":
    input_file = '/mnt/data/Media/temp/small.mp4'
    output_file = '/mnt/data/Media/temp/small.mkv'
    os.remove(output_file)
    convert_to_x265(input_file, output_file)
    input_file = '/mnt/data/Media/temp/large.mp4'
    output_file = '/mnt/data/Media/temp/large.mkv'
    os.remove(output_file)
    convert_to_x265(input_file, output_file)
