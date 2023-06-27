# File: /cherryAI/code_executor.py

import subprocess

def execute_python_code(code):
    """
    This function takes a string of python code, saves it to a temporary file, 
    executes it and returns the output.
    """
    with open('temp.py', 'w') as file:
        file.write(code)
        
    try:
        # Use the subprocess module to execute the file and capture the output
        output = subprocess.check_output(["python", "temp.py"])
    except subprocess.CalledProcessError as e:
        output = e.output

    return output
