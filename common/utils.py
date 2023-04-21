from pathlib import Path
import os


def clear_debug_logs():
    """
    Removes all debug logs that do not contain the string "Error".

    This function searches for all files in the current directory whose filename contains the word "debug".
    If a file is found, its contents are checked for the presence of the word "Error".
    If the word "Error" is not found in the file, the file is deleted.
    :return: None
    """
    for file in Path().absolute().iterdir():
        filename = os.path.basename(file)
        if "debug" in filename:
            with open(file) as f:
                file_content = f.read()
                if "Error" not in file_content:
                    os.remove(file)
