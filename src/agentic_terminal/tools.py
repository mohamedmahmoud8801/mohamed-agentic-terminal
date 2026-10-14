from fastmcp import FastMCP
import re
from pathlib import Path

mcp = FastMCP()

@mcp.tool()
def bash(command:str):
    '''This function will execute a bash command and return the output. This function
    is useful for executing bash commands including creating files, directories, and other bash commands.'''
    import subprocess
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.stderr.decode('utf-8')


@mcp.tool()
def python_code(code:str):
    '''This function will execute a python code and return the output.'''
    import subprocess
    try:
        result = subprocess.run(['python', '-c', code], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.stderr.decode('utf-8')

@mcp.tool()
def python_file(file:str):
    '''This function will execute a python file and return the output.'''
    import subprocess
    try:
        result = subprocess.run(['python', file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.stderr.decode('utf-8')

@mcp.tool()
def glob(pattern:str):
    '''This function will return a list of files that match the given pattern. This function is useful for finding files in a directory.'''
    import glob
    return glob.glob(pattern)


@mcp.tool()
def grep(pattern: str, file: str):
    """
    Search for a pattern in a file and return matching lines.
    Works on Windows and Ubuntu.
    """
    try:
        path = Path(file)

        if not path.is_file():
            return f"Error: File '{file}' does not exist."

        matches = []

        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line_number, line in enumerate(f, start=1):
                if re.search(pattern, line):
                    matches.append(f"{line_number}: {line.rstrip()}")

        if matches:
            return "\n".join(matches)

        return "No matching lines found."

    except re.error as e:
        return f"Invalid regular expression: {e}"

    except OSError as e:
        return f"File error: {e}"

@mcp.tool()
def read_file(file:str):
    '''This function will read the contents of a file and return it as a string.'''
    try:
        with open(file, 'r') as f:
            return f.read()
    except Exception as e:
        return str(e)

@mcp.tool()
def write_file(file:str, content:str):
    '''This function will write the given content to a file. If the file does not exist, it will be created.'''
    try:
        with open(file, 'w') as f:
            f.write(content)
        return f"Content written to {file} successfully."
    except Exception as e:
        return str(e)

@mcp.tool()
def create_folder(folder:str):
    '''This function will create a folder with the given name. If the folder already exists, it will return a message indicating that the folder already exists.'''
    import os
    try:
        os.makedirs(folder)
        return f"Folder '{folder}' created successfully."
    except FileExistsError:
        return f"Folder '{folder}' already exists."
    except Exception as e:
        return str(e)

@mcp.tool()
def delete_folder(folder:str):
    '''This function will delete a folder with the given name. If the folder does not exist, it will return a message indicating that the folder does not exist.'''
    import shutil
    import os
    try:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            return f"Folder '{folder}' deleted successfully."
        else:
            return f"Folder '{folder}' does not exist."
    except Exception as e:
        return str(e)
