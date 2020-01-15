import sys
import os


def return_path(original_path, file_name):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = original_path

    return os.path.join(base_path, file_name)
