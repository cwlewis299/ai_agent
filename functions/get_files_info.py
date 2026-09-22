import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        try:
            absolute_working_directory = os.path.abspath(working_directory)
        except Exception as e:
            err_message = ValueError(f'Error: Invalid working directory "{working_directory}"')

        try:
            target_full_path = os.path.normpath(os.path.join(absolute_working_directory, directory))
        except Exception as e:
            err_message = ValueError(f'Error: Invalid target directory "{directory}"')

        if not os.path.isdir(target_full_path):
            err_message = ValueError(f'Error: "{directory}" is not a directory')

        valid_target_dir = os.path.commonpath([absolute_working_directory, target_full_path]) == absolute_working_directory
        if not valid_target_dir:
            err_message = ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    except Exception as e:
        err_message = ValueError(f'Error: An unexpected error occurred')

    if 'err_message' in locals():
        return f"Result for '{directory}' directory:\n    {str(err_message)}"

    if directory == ".":
        normalized_directory = "current"
    else:
        normalized_directory = os.path.normpath(directory)

    target_directory_contents = {}
    for obj in os.listdir(target_full_path):
        if obj.startswith('__') and obj.endswith('__'):
            continue
        obj_full_path = os.path.join(target_full_path, obj)
        target_directory_contents[obj] = {
            "is_dir": os.path.isdir(obj_full_path),
            "size": os.path.getsize(obj_full_path)
        }

    content_str = "\n  - ".join([f"{name}: file_size={info['size']}, is_dir={info['is_dir']}" for name, info in target_directory_contents.items()])   

    return f'Result for {normalized_directory} directory:\n  - {content_str}'
