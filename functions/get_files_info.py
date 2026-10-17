import os

#This is setting up guardrails for the agent to stay in the working directory
def get_files_info(working_directory: str, directory: str = ".") -> str:
    #Working directory absolute path
    working_dir_abs = os.path.abspath(working_directory)
    
    #Target directory path
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    
    #Check if Working directory path and target directory path shares a common path
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    
    #If not a valid directory
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
    #If directory doesnt exist
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    #Empty string
    file_list_string = ""
    
    #A for loop for all the things in the list inside target directory
    for name in os.listdir(target_dir):
        filepath = os.path.join(target_dir, name)
        file_list_string += f"- {name}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}\n"
    
    #If no problems
    return file_list_string
    
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
