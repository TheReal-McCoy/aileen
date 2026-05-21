import os
from config import MAX_CHARS
from google.genai import types

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
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a file in a specified directory relative to the working directory, providing file contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to read file from, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)