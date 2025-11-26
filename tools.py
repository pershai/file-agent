import os

read_file_definition = {
    "name": "read_file",
    "description": "Reads a file and returns its contents.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "file_path": {
                "type": "STRING",
                "description": "The path to the file to read. Supports relative paths and user expansion (e.g., ~/)."
            }
        },
        "required": ["file_path"]
    }
}

list_dir_definition = {
    "name": "list_dir",
    "description": "List the contents of a directory",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "directory_path": {
                "type": "STRING",
                "description": "The path to the directory to list. Supports relative paths and user expansion (e.g., ~/)."
            }
        },
        "required": ["directory_path"]
    }
}

write_file_definition = {
    "name": "write_file",
    "description": "Write contents to a file",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "file_path": {
                "type": "STRING",
                "description": "The path to the file to write. Supports relative paths and user expansion (e.g., ~/)."
            },
            "contents": {
                "type": "STRING",
                "description": "The contents to write to the file"
            }
        },
        "required": ["file_path", "contents"]
    }
}

def read_file(file_path: str) -> str:
    try:
        full_path = os.path.abspath(os.path.expanduser(file_path))
        with open(full_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {e}"

def write_file(file_path: str, contents: str) -> str:
    try:
        full_path = os.path.abspath(os.path.expanduser(file_path))
        with open(full_path, "w") as f:
            f.write(contents)
        return f"Successfully wrote to {full_path}"
    except Exception as e:
        return f"Error writing file {file_path}: {e}"

def list_dir(directory_path: str) -> list[str]:
    try:
        full_path = os.path.abspath(os.path.expanduser(directory_path))
        return os.listdir(full_path)
    except Exception as e:
        return [f"Error listing directory {directory_path}: {e}"]

file_tools = {
    "read_file": {"definition": read_file_definition, "function": read_file},
    "write_file": {"definition": write_file_definition, "function": write_file},
    "list_dir": {"definition": list_dir_definition, "function": list_dir}
}
