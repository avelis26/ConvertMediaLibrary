#!/usr/bin/env python3
import ffmpeg

def convert_to_x265(input_file, output_file):
    (
        ffmpeg
        .input(input_file)
        .output(output_file, vcodec='hevc_nvenc', preset='slow', crf=23, c='copy')
        .run()
    )
if __name__ == "__main__":
    input_file = '/mnt/data/Media/temp/small.mp4'
    output_file = '/mnt/data/Media/temp/small.mkv'
    convert_to_x265(input_file, output_file)
