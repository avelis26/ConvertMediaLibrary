# ConvertMediaLibrary

Python scripts to automate converting all h264 videos to h265.

## Basic order of operations:
* `Vilicus.py`:
    - loads `parameters.json`.
    - creates (if not exist) working directory `log_parent_path` and deletes manifest (if exists).
    - scans files larger than `min_file_size` recursivley starting at `movies_parent_path`.
    - adds non-h265 files found to manifest `movies_manifest_filename`.
    - reads each line in the manifest and calls a convert function using ffmpeg.

### Author
- [Graham Pinkston](https://github.com/avelis26)
- [Execute python in background via SSH](https://janakiev.com/blog/python-background/)