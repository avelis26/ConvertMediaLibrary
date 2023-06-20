# Summary

* I wrote this Python script to automate converting all non-h265 videos to h265 for space saving on my **Plex** server.
* I tried using the Nvida GPU-accelerated version of **ffmpeg**, and while the conversion was 10x to 20x faster, the file sizes where often much larger.
* This script can be executed from the terminal as a background job, or from cron.
* The `parameters_<name>.json` file in the repository is used to configure the script.
* I use `__min_file_size__` as a fast filter to prevent using **ffmpeg** probe on non-video files.
* **Replace `/home/avelis/` with your home directory.**
* **Replace `/home/avelis/source/` with the location where you cloned the repository.**

## Order Of Operations:
* From the cron:
    - `crontab -e`
    - Append:
        - `@reboot cd /home/avelis/source/ConvertMediaLibrary && ./Vilicus.py --paramfile 'parameters_movies.json' > /home/avelis/movies_output.log 2>&1`
        - `@reboot cd /home/avelis/source/ConvertMediaLibrary && ./Vilicus.py --paramfile 'parameters_shows.json' > /home/avelis/shows_output.log 2>&1`
* From the terminal:
    - `cd /home/avelis/source/ConvertMediaLibrary && nohup ./Vilicus.py -p 'parameters_movies_temp.json' > /home/avelis/movies_temp_output.log 2>&1 &`
    - `cd /home/avelis/source/ConvertMediaLibrary && nohup ./Vilicus.py -p 'parameters_movies.json' > /home/avelis/movies_output.log 2>&1 &`
    - `cd /home/avelis/source/ConvertMediaLibrary && nohup ./Vilicus.py -p 'parameters_shows.json' > /home/avelis/shows_output.log 2>&1 &`
* `Vilicus.py`:
    - loads `parameters_<name>.json`.
    - creates (if not exist) working directory `__log_parent_path__` and deletes manifest (if exists).
    - scans files larger than `__min_file_size__` recursivley starting at `__videos_parent_path__`.
    - adds non-h265 files found to manifest `__manifest_filename__`.
    - reads each line in the manifest and calls **ffmpeg** to convert the file to h265.
	- logs progress and metrics to `__log_filename__`.
* To request that the script exit after the current conversion:
    - `cd __log_parent_path__`
	- `touch __exit_filename__`
	- The script will see the exit file and exit after the current conversion completes.

### Author
- [Graham Pinkston](https://github.com/avelis26)
- [ChatGPT4](https://chat.openai.com/)
