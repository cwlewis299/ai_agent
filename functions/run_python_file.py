import os, subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        absolute_working_directory = os.path.abspath(working_directory)
    except Exception as e:
        return ValueError(f'Error: Invalid working directory "{working_directory}": {str(e)}')

    try:
        target_full_path = os.path.normpath(os.path.join(absolute_working_directory, file_path))
    except Exception as e:
        return ValueError(f'Error: Invalid target directory "{file_path}": {str(e)}')

    valid_target_dir = os.path.commonpath([absolute_working_directory, target_full_path]) == absolute_working_directory
    if not valid_target_dir:
        return ValueError(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

    if not os.path.isfile(target_full_path):
        return ValueError(f'Error: "{file_path}" does not exist or is not a regular file')

    if not target_full_path.endswith('.py'):
        return ValueError(f'Error: "{file_path}" is not a Python file')

    try:

        command = ["python", target_full_path]
        if args:
            command.extend(args)
        #print(f"extended commands: {command}")
        result = subprocess.run(command, cwd=absolute_working_directory, capture_output=True, text=True, timeout=30)
        #print(result)
        #print(result.returncode)
        #print(f"stdout: {bool(result.stdout)}")
        #print(f"stderr: {bool(result.stderr)}")
        
        if result.returncode != 0:
            output: str = f'Process exited with code {result.returncode}'
        if not result.stdout and not result.stderr:
            output: str = "No output produced"
        if result.stdout:
            output: str = f"STDOUT: {result.stdout}"
        if result.stderr:
            output: str = f"STDERR: {result.stderr}"
        #print(f" output: bool(output)")
        return output
    except Exception as e:
        return ValueError(f'Error: executing Python file: {e}')