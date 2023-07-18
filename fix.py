#!/usr/bin/env python3
import re
import os

def extract_data(log_file):
    with open(log_file, 'r') as f:
        log_data = f.read()
    pattern = r'Failed to convert file: (.*)'
    matches = re.findall(pattern, log_data)
    return matches

if __name__ == "__main__":
    log_file = 'fix.log'
    extracted_data = extract_data(log_file)
    for file_path in extracted_data:
        # Delete the file with the ".mkv" extension
        mkv_file = os.path.splitext(file_path)[0] + '.mkv'
        if os.path.exists(mkv_file):
            os.remove(mkv_file)
            print(f"Deleted {mkv_file}")
        # Rename the file with the ".old" extension
        old_file = file_path + '.old'
        if os.path.exists(old_file):
            os.rename(old_file, file_path)
            print(f"OLD: {old_file}")
            print(f"NEW: {file_path}")
            print("\n")
