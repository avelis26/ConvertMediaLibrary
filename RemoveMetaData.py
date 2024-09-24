#!/usr/bin/env python3

import os
import sys

# ANSI escape sequences for colors
COLORS = {
    '.jpg': '\033[93m',   # Yellow
    '.nfo': '\033[92m',   # Green
    '.png': '\033[94m',   # Blue
    '.srt': '\033[95m',   # Magenta
    '.mp3': '\033[96m',   # Cyan
    '.xml': '\033[90m',   # Grey
    'reset': '\033[0m',   # Reset
    'error': '\033[91m'   # Red for errors
}

def search_and_delete_files(directory):
    # List of target extensions
    target_extensions = {'.jpg', '.nfo', '.png', '.srt', '.mp3', '.xml', '.txt', '.htm', '.html', '.json'}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in target_extensions:
                file_path = os.path.join(root, file)
                color = COLORS.get(ext.lower(), COLORS['reset'])
                print(f"{color}{file_path}{COLORS['reset']}")
                try:
                    os.remove(file_path)
                    print(f"{color}Deleted: {file_path}{COLORS['reset']}")
                except Exception as e:
                    print(f"{COLORS['error']}ERROR DELETING FILE: {file_path}{COLORS['reset']}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.isdir(directory_path):
        print("Invalid directory path.")
        sys.exit(1)

    search_and_delete_files(directory_path)
