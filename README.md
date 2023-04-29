# Directory TimeStamp

Directory TimeStamp is a Python script that timestamps all files, folders, and subdirectories in a given directory. This script can be useful for keeping track of the duration of files in each directory and subdirectories.

## Features

- **Pattern and mark removal:** The script can remove patterns and marks from file and folder names, allowing for cleaner timestamps.

- **Zero padding:** Directory TimeStamp can add zero padding to the names of files and folders, creating a more uniform naming convention.

- **Timestamp removal:** If timestamps have already been applied, the script can remove them to prevent duplication.

- **Multi-directory support:** The script can process multiple directories and generate logs for each one, allowing for easy tracking of changes across multiple projects or systems.

## Usage

1. Clone the repository.
2. Install the required packages: [ffmpeg](https://ffmpeg.org/download.html)
3. Run the script: `python directory_timestamp.py`
4. Enter the `<paths_to_the_directories>`
5. `exit` to stop
6. The script will output a log file with the timestamps for each file, folder, and subdirectory in the given directory.

## Colab Demo

Check out this [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ankitsamaddar/directory-timestamp/) to see how the script works with your directory.



## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.

## Acknowledgments

Special thanks to the developers of the Python programming language and the ffmpeg library, which is used in this script for fetching the duration.
