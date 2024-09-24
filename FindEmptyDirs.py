#!/usr/bin/env python3
import os
import sys
import argparse
import shutil

def get_directory_size(path):
    """Calculate the total size of the directory in megabytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size / (1024 * 1024)  # Convert size to megabytes

def find_empty_or_small_directories(path, size_threshold, delete=False):
    """Find directories that are empty or smaller than the given size threshold."""
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        # Check if the directory is empty
        if not os.listdir(dirpath):
            print(f"Empty directory: {dirpath}")
            if delete:
                try:
                    os.rmdir(dirpath)
                    print(f"Deleted empty directory: {dirpath}")
                except Exception as e:
                    print(f"Error deleting directory {dirpath}: {e}")
        else:
            dir_size = get_directory_size(dirpath)
            if dir_size < size_threshold:
                print(f"Directory {dirpath} is smaller than {size_threshold} MB ({dir_size:.2f} MB)")
                if delete:
                    try:
                        shutil.rmtree(dirpath)
                        print(f"Deleted directory: {dirpath} (Size: {dir_size:.2f} MB)")
                    except Exception as e:
                        print(f"Error deleting directory {dirpath}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find and optionally delete empty or small directories.")
    
    parser.add_argument("--path", required=True, help="Path to the directory to search")
    parser.add_argument("--minsize", type=float, required=True, help="Minimum size (in MB) for directories to keep")
    parser.add_argument("--delete", choices=['yes', 'no'], default='no', help="Whether to delete found directories (yes/no)")

    args = parser.parse_args()

    # Check if the provided path is valid
    if not os.path.isdir(args.path):
        print(f"Error: {args.path} is not a valid directory.")
        sys.exit(1)

    # Convert delete argument to boolean
    delete = args.delete.lower() == 'yes'

    # Find and optionally delete empty or small directories
    find_empty_or_small_directories(args.path, args.minsize, delete)
