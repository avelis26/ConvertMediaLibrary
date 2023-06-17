import os
import ffmpeg
from pathlib import Path

def main():
    source_directory = input("Enter source directory: ")
    destination_directory = input("Enter destination directory: ")
    log_file = input("Enter log file path (optional): ")

    if not os.path.isdir(source_directory) or not os.path.isdir(destination_directory):
        print("Invalid source or destination directory.")
        return

    if log_file:
        log_file = open(log_file, "w")

    log_progress(log_file, "Conversion Progress:\n")

    for root, _, files in os.walk(source_directory):
        for file in files:
            source_path = os.path.join(root, file)
            if is_video_file(source_path) and not is_encoded_with_h265(source_path):
                destination_path = os.path.join(destination_directory, get_hevc_filename(file))
                convert_media_file(source_path, destination_path)
                log_progress(log_file, f"Converted: {source_path}\n")

    total_saved_space = ffmpeg.probe(destination_directory)["format"]["size"]
    log_progress(log_file, f"Total Saved Space: {total_saved_space / (1024 * 1024)} MB\n")
    log_progress(log_file, f"Completed Conversions: {completed_conversions}\n")

    if log_file:
        log_file.close()

def is_video_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in [".mp4", ".mkv", ".avi", ".mov"]

def is_encoded_with_h265(file_path):
    try:
        probe = ffmpeg.probe(file_path)
        video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
        return any(stream["codec_name"].lower() == "hevc" for stream in video_streams)
    except ffmpeg.Error:
        return False

def convert_media_file(source_path, destination_path):
    ffmpeg.input(source_path).output(destination_path, vcodec="libx265", crf=28, acodec="copy").run()
    completed_conversions += 1

def get_hevc_filename(filename):
    file_name, file_extension = os.path.splitext(filename)
    return f"{file_name}_hevc{file_extension}"

def log_progress(log_file, message):
    if log_file:
        log_file.write(message)
    print(message, end="")

if __name__ == "__main__":
    main()
