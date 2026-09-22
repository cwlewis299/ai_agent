import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        try:
            absolute_working_directory = os.path.abspath(working_directory)
        except Exception as e:
            return ValueError(f'Error: Invalid working directory "{working_directory}"')

        try:
            target_full_path = os.path.normpath(os.path.join(absolute_working_directory, directory))
        except Exception as e:
            return ValueError(f'Error: Invalid target directory "{directory}"')

        if not os.path.isdir(target_full_path):
            return ValueError(f'Error: "{directory}" is not a directory')

        valid_target_dir = os.path.commonpath([absolute_working_directory, target_full_path]) == absolute_working_directory
        if not valid_target_dir:
            return ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    except Exception as e:
        return ValueError(f'Error: An unexpected error occurred')

    return f'Success: "{directory}" is within the working directory'
