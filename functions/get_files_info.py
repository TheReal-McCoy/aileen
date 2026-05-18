import os

def get_files_info(working_directory, directory="."):
    try:
        work_dir_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(work_dir_path, directory))
        if os.path.commonpath([work_dir_path, full_path]) != work_dir_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        files_info = []
        for filename in os.listdir(full_path):
            filepath = os.path.join(full_path, filename)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"
    

