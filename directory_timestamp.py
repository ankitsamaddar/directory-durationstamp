"""
Directory TimeStamp: TimeStamp All Files,Folders and Subdirectories
TODO: convert in ipynb with more functions and implement form
TODO: implement add time to subtitles also
TODO: convert to module to directly access from shell
"""
# ADD MARKS IN LINE 48
__author__ = "ankitsamaddar"

import re
import subprocess
import os


def get_video_length(file_path):
    result = subprocess.run(["ffmpeg", "-i", file_path],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stderr.decode()
    duration_index = output.find("Duration: ")
    if duration_index != -1:
        duration_str = output[duration_index + 10:duration_index + 18]
        hours, minutes, seconds = map(int, duration_str.split(':'))
        duration = (hours * 3600) + (minutes * 60) + seconds
        return duration
    else:
        return 0


def time_get(duration):
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds


def file_check(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm",
                        ".mpeg", ".mpg", ".3gp", ".m4v", ".ogv", ".qt", ".rm", ".swf", ".vob", ".ts"]
    audio_extensions = [".mp3", ".wav", ".aac", ".m4a", ".wma", ".flac", ".opus",
                        ".ogg", ".amr", ".aiff", ".au", ".mka", ".mpc", ".ra", ".snd", ".wv"]
    all_extensions = video_extensions+audio_extensions
    if ext in all_extensions:
        return True
    return False


def remove_mark_and_padding(f_path):
    # Marks to remove
    marks = ['', '']
    # Escape the special characters in each mark
    special_characters = ['\\', '^', '$', '.',
                          '?', '*', '+', '|', '(', ')', '[', ']']
    escaped_marks = []
    for mark in marks:
        for character in special_characters:
            mark = mark.replace(character, '\\' + character)
        escaped_marks.append(mark)
    # Spliting name and extension
    f_name = os.path.basename(f_path)
    # 01. Mark Replacement
    for mark in escaped_marks:
        f_name = re.sub(mark, "", f_name)
    # 02. Remove If Time Already added
    t_marks = [r'(\s[•▸]\s*)(.{4}|.{0})(\d{2}m\d{2}s)',
               r'\s{2}(\d{2}hr|.{0})(\d{2}m\d{2}s)',
               r'(\s+-\s+)(\d{2}h|.{0})(\d{2}m\d{2}s)', r'_(\d{2}h|.{0})(\d{2}m\d{2}s)']
    for t_mark in t_marks:
        f_name = re.sub(t_mark, "", f_name)
    # 03. Zero Padding
    num_digits = 2  # number of digits to zero-fill
    f_name = re.sub(
        r'^[\d]+', lambda match: match.group(0).zfill(num_digits), f_name)

    new_f_path = os.path.join(os.path.dirname(f_path), f_name)

    return new_f_path


def add_name(path, length):
    folder_name = remove_mark_and_padding(os.path.basename(path))
    if length > 0:
        hours, minutes, seconds = time_get(length)
        if hours > 0:
            folder_name = f"{folder_name} - {hours:02d}h{minutes:02d}m{seconds:02d}s"
        else:
            folder_name = f"{folder_name} - {minutes:02d}m{seconds:02d}s"
        new_path = os.path.join(os.path.dirname(path), folder_name)
        os.rename(path, new_path)
        print(f"Processed. New Dirname: {folder_name}")
    elif folder_name != os.path.basename(path):
        new_path = os.path.join(os.path.dirname(path), folder_name)
        os.rename(path, new_path)
        print(f"Processed. New Dirname: {folder_name}")


def add_length_to_filename(file_path):
    length = get_video_length(file_path)
    if length > 0:
        hours, minutes, seconds = time_get(length)
        file_name = remove_mark_and_padding(os.path.splitext(file_path)[0])
        parent_folder = os.path.dirname(file_path)
        ext = os.path.splitext(file_path)[1].lower()
        if hours > 0:
            new_file_name = f"{file_name}_{hours:02d}h{minutes:02d}m{seconds:02d}s{ext}"
        else:
            new_file_name = f"{file_name}_{minutes:02d}m{seconds:02d}s{ext}"
        new_path = os.path.join(parent_folder, new_file_name)
        os.rename(file_path, new_path)
    return length


def add_length_to_foldername(folder_path, length=0):
    file_num = 1
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and file_check(file_path):
            length += add_length_to_filename(file_path)
            file_num += 1
    folder_name = remove_mark_and_padding(os.path.basename(folder_path))
    if length > 0:
        hours, minutes, seconds = time_get(length)
        if hours > 0:
            folder_name = f"{folder_name} - {hours:02d}h{minutes:02d}m{seconds:02d}s"
        else:
            folder_name = f"{folder_name} - {minutes:02d}m{seconds:02d}s"
        new_path = os.path.join(os.path.dirname(folder_path), folder_name)
        os.rename(folder_path, new_path)
        print(f"Processed. New foldername: {folder_name}")
    elif folder_name != os.path.basename(folder_path):
        new_path = os.path.join(os.path.dirname(folder_path), folder_name)
        os.rename(folder_path, new_path)
        print(f"Processed. New foldername: {folder_name}")

    return length


def process_directory(path):
    total_length = 0
    for dirpath, dirnames, filenames in os.walk(path):
        dir_num, folder_num = 1, 1
        for dirname in dirnames:
            folder_path = os.path.join(dirpath, dirname)
            if any(os.path.isdir(os.path.join(folder_path, item)) for item in os.listdir(folder_path)):
                # if folder_path contains subdirectories
                print(
                    f"\nDirectory[{dir_num:02d}]: {os.path.basename(dirname)}\tRoot: {os.path.basename(dirpath)}")
                dir_num += 1
                total_length += process_directory(folder_path)
            else:
                print(
                    f"\nFolder[{folder_num:02d}]: {os.path.basename(dirname)}\tRoot: {os.path.basename(dirpath)}")
                folder_num += 1
                total_length += add_length_to_foldername(folder_path)
        # Files inside directory with subdirectories
        if filenames:
            folder_path = os.path.dirname(os.path.join(dirpath, filenames[0]))
            print(f"\nRoot: {os.path.basename(dirpath)}")
            total_length += add_length_to_foldername(folder_path, total_length)
            break
        add_name(dirpath, total_length)
        break  # return to previous call
    return total_length


def control(path, path_num):
    try:
        if os.path.exists(path):
            total_length = process_directory(path)
            """
            hours, minutes, seconds = time_get(total_length)
            if total_length > 0:
                if hours > 0:
                    dir_name = f"{dir_name} - {hours:02d}h{minutes:02d}m{seconds:02d}s"
                else:
                    dir_name = f"{dir_name} - {minutes:02d}m{seconds:02d}s"
                new_path = os.path.join(os.path.dirname(path), dir_name)
                os.rename(path, new_path)"""
            print(f"\nProcessed. [{path_num}] Root Directory!")
        else:
            print(f"Error! Invalid path: {path}")
    except Exception as e:
        print("An error occurred: ", e)


def main():
    paths = []
    while True:
        path = input("Enter the path or type 'exit' to stop: ")
        if path == "exit":
            break
        paths.append(path)

    for path in paths:
        path_num = int(paths.index(path))  # not returning+1
        path_num += 1
        print(f"Root Directory: {path_num}: {os.path.basename(path)}")
        control(path, paths.index(path))


if __name__ == "__main__":
    main()
