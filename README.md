# ConvertMediaLibrary

Python scripts to automate converting all h264 videos to h265.

## Basic order of operations:
* Cron calls `Vilicus.py`.
* `Vilicus.py` calls `CreateConversionManifest.py` and creates a list of all h264 videos found.
* `Vilicus.py` reads h264 manifest and calls `ConvertToH265.py` for each file.