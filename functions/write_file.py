import os
from google.genai import types

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
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="verifies a file exists, and writes to it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to file to be written to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to write to the file_path"
            )
        },
    required=["file_path", "content"]
    ),
)
