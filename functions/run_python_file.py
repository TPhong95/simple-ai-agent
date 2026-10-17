import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    #Working directory absolute path
    working_dir_abs = os.path.abspath(working_directory)
    
    #Target file path
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
    #Check if Working directory path and target file path shares a common path
    valid_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
    
    #If not a valid file path
    if not valid_file_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    #If file does not exist and is not a file
    if not os.path.isfile(target_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file_path]
    if args:
        command.extend(args)
    
    result = subprocess.run(
        command, 
        cwd = os.path.dirname(target_file_path),
        capture_output=True,
        text=True,
        timeout=30)
        
    output = []
    
    if result.returncode != 0:
        output.append(f"Process exited with code {result.returncode}")
    
    if not result.stdout and not result.stderr:
        output.append("No output produced")
    else:
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")
     
    return "\n".join(output)
    
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a .py file which are python file on the file path specified with optional args parameters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path to the specific file to run, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional list of command-line arguments to pass to the python file"
                },
            },
            "required": ["file_path"],
        },
    },
}
