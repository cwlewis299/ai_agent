import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        try:
            absolute_working_directory = os.path.abspath(working_directory)
        except Exception as e:
            return ValueError(f'Error: Invalid working directory "{working_directory}"')

        try:
            os.makedirs(file_path, exist_ok=True) # create dir structure for target file
        except Exception as e:
            return ValueError(f'Error: Invalid target directory "{file_path}": {str(e)}')
        try:
            target_full_path = os.path.normpath(os.path.join(absolute_working_directory, file_path))
        except Exception as e:
            return ValueError(f'Error: Invalid target directory "{file_path}": {str(e)}')

        if os.path.isdir(target_full_path):
            return ValueError(f'Error: Cannot write to "{file_path}" as it is a directory')

        valid_target_dir = os.path.commonpath([absolute_working_directory, target_full_path]) == absolute_working_directory
        if not valid_target_dir:
            return ValueError(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    
    except Exception as e:
        return ValueError(f'Error: An unexpected error occurred: {str(e)}')

    # Removed error message check as all errors are now returned immediately

    try:
        with open(target_full_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: writing to '{file_path}': {str(e)}"

# LLM declaration schema
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Modifies or creates a specified file (path) with a given text "
        "If creating a new file, any required directories are also created",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write, relative to the working directory"
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file."
                },
            },
            "required": ["file_path", "content"],
        },
    },
}