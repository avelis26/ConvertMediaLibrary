# Summary

* Python script to automate converting all non-h265 videos to h265 for space saving.
* I tried using the Nvida GPU-accelerated version of **ffmpeg**, and while the conversion was 10x to 20x faster, the file sizes ofter where larger, sometimes much larger.
* This script can be executed from the terminal as a background job, or from cron.
* The `parameters.json` file in the repository is used to configure the script.
* I use `min_file_size` as a fast filter to prevent using **ffmpeg** probe on non-video files.

## Order Of Operations:
* `crontab -e`
    - Append: `@reboot cd /home/avelis/source/ConvertMediaLibrary && ./Vilicus.py > /home/avelis/vilicus/output.log 2>&1`
* `Vilicus.py`:
    - loads `parameters.json`.
    - creates (if not exist) working directory `log_parent_path` and deletes manifest (if exists).
    - scans files larger than `min_file_size` recursivley starting at `movies_parent_path`.
    - adds non-h265 files found to manifest `movies_manifest_filename`.
    - reads each line in the manifest and calls **ffmpeg** to convert the file to h265.
	- logs progress and metrics to `log_filename`.

### Author
- [Graham Pinkston](https://github.com/avelis26)
- [Ai Used To Improve This Code](https://chat.openai.com/)
