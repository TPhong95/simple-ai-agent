import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    #Working directory absolute path
    working_dir_abs = os.path.abspath(working_directory)
    
    #Target file path
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
    #Check if Working directory path and target file path shares a common path
    valid_file_path = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    
    #If not a valid file path
    if not valid_file_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    #If file does not exist and is not a file
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
        
    #Reads until max char from config file in root. Default 10000 and using with statement closes file after block finishes and keeps the file_content_string in memory
    with open(target_file, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        #If there's more then 
        if f.read(1):
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    return file_content_string
    
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the content of a file in a specified file path relative to the working directory, with a maximum of 10000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path to the specific file to read from, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["file_path"],
        },
    },
}
