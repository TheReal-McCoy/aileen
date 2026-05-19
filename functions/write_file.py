import os

def write_file(working_directory, file_path, content):
    onepath = os.path.join(working_directory, file_path)
    mpath = os.path.abspath(onepath)
    wdir = os.path.abspath(working_directory)
    try:
        if os.path.commonpath([wdir, mpath]) != wdir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(mpath):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(mpath) ,exist_ok=True)
        with open(mpath, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"