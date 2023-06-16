# ConvertMediaLibrary

Python scripts to automate converting all h264 videos to h265.

## Question Proposed To ChatGPT:
* Please improve this script: https://github.com/avelis26/ConvertMediaLibrary/blob/main/Vilicus.py with the main objective being to search a source directory recursively for video files not encoded with h265, append those files to a manifest, and use multi-threading with FFmpeg to convert those files to h265 while reporting progress to a log file with details like total space saved so far and number of conversions completed.

## ChatGPT Summary
- Here's a summary of the changes made to the script:
1. Introduced global variables total_saved_space and completed_conversions to track the conversion progress.
2. Modified the convert_media_file function to calculate the saved space by comparing the sizes of the original file and the converted file.
3. Updated the convert_media_file function to update the global variables for the total saved space and completed conversions.
4. Modified the convert_media_library function to use a ThreadPoolExecutor for concurrent conversion of video files.
5. Added a log file as an additional command-line argument (-l or --log-file) to specify the path for the log file. The log file will contain the conversion progress and details such as the converted file paths, total saved space, and completed conversions.
6. Updated the main function to include the new --log-file argument and call the convert_media_library function with the specified source directory, destination directory, and log file path.

Now, the script will recursively search the source directory for video files not encoded with H.265/HEVC, convert them using multi-threading with FFmpeg, and report the progress and details to the specified log file.

### Author
- [Graham Pinkston](https://github.com/avelis26)
- [Ai Used To Write This Code](https://chat.openai.com/)
