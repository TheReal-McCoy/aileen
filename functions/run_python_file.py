import os
import subprocess
from google.genai import types

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    o_path = os.path.join(working_directory, file_path)
    m_path = os.path.abspath(o_path)
    wdir_path = os.path.abspath(working_directory)
    try:
        if os.path.commonpath([wdir_path, m_path]) != wdir_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(m_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not m_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", m_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=wdir_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_parts = []
        if result.returncode:
            output_parts.append(f"Process exited with code {result.returncode}")
        if result.stdout:
            output_parts.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output_parts.append(f"STDERR: {result.stderr}")
        if result.stdout == "" and result.stderr == "":
            return "No output produced"
        
        return "\n".join(output_parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Makes sure a file exists, ends in .py, and runs it, displaying the output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to run files from, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="args passed in extend the command",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    required=["file_path"],
    ),
)