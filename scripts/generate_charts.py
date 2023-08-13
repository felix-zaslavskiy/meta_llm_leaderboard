
import subprocess

def run_script(script_name, save_to_file=False):
    """
    Run a python script and optionally pass an argument to it.

    Parameters:
    - script_name (str): Name of the python script to run.
    - save_to_file (bool): Whether to save the output to a file or not.

    Returns:
    - int: Return code after executing the script. Typically, 0 means success and non-zero means some error occurred.
    """
    command = ["python", script_name]

    if save_to_file:
        command.append("--save_to_file")

    result = subprocess.run(command)

    return result.returncode