from functions.get_files_info import get_files_info
import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        try:
            absolute_working_directory = os.path.abspath(working_directory)
        except Exception as e:
            return ValueError(f'Error: Invalid working directory "{working_directory}"')

        try:
            target_full_path = os.path.normpath(os.path.join(absolute_working_directory, file_path))
        except Exception as e:
            err_message = ValueError(f'Error: Invalid target file path "{file_path}"')

        if not os.path.isfile(target_full_path):
            err_message = ValueError(f'Error: File not found or is not a regular file: "{file_path}"')

        valid_target_file = os.path.commonpath([absolute_working_directory, target_full_path]) == absolute_working_directory
        if not valid_target_file:
            err_message = ValueError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        
        if 'err_message' in locals():
            return f"{str(err_message)}"
        
        
        MAX_CHARS = 10000
        try:
            file = open(target_full_path, 'r')
            content: str = file.read(MAX_CHARS)  # Read the first MAX_CHARS characters
        except Exception as e:
            err_message = ValueError(f'Error: Unable to read file "{file_path}"')
        
        if file.read(1):  # Check if there's more content beyond MAX_CHARS
            content += f'[...File "{file_path} truncated at {MAX_CHARS} characters]'
    
    except Exception as e:
        err_message = ValueError(f'Error: An unexpected error, {str(e)}, occurred while reading the file "{file_path}"')
    

    if 'err_message' in locals():
        return f"{str(err_message)}"
    return content