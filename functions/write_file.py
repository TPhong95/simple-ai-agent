import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    #Working directory absolute path
    working_dir_abs = os.path.abspath(working_directory)
    
    #Target file path
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
    #Check if Working directory path and target file path shares a common path
    valid_file_path = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    
    #If not a valid file path
    if not valid_file_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    #If file path is a directory
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    #Creates directories if there a missing directories in the file path
    parent_dir = os.path.dirname(target_file)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    
    with open(target_file, "w") as f:
        f.write(content)
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to the file in the file path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path to the specific file to write to, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "The string to write to the file that are specified on the file_path"
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
