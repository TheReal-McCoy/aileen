import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    onepath = os.path.join(working_directory, file_path)
    mpath = os.path.abspath(onepath)
    wdir = os.path.abspath(working_directory)
    try:
        if os.path.commonpath([wdir, mpath]) != wdir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(mpath):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(mpath, "r") as f:
            contents = f.read(MAX_CHARS)
            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return contents
    except Exception as e:
        return f"Error: problem reading file - {e}"