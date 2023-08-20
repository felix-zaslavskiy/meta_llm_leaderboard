import subprocess
import json
import datetime

def run_script(script_name, save_to_file=False, global_config=None):
    """
    Run a python script and optionally pass an argument to it.

    Parameters:
    - script_name (str): Name of the python script to run.
    - save_to_file (bool): Whether to save the output to a file or not.
    - global_config (dict): A dictionary containing global configurations.

    Returns:
    - int: Return code after executing the script. Typically, 0 means success and non-zero means some error occurred.
    """
    command = ["python", script_name]

    if save_to_file:
        command.append("--save_to_file")

    if global_config:
        command.extend(["--global_config", json.dumps(global_config)])

    result = subprocess.run(command)

    return result.returncode

today = datetime.datetime.now()
global_config = {
    "CHART_TAG": "@FZaslavskiy",
    "DATETIME": today.strftime('%Y%m%d_%H%M')
}

scripts_to_run = ["hf_llm_diagramv2.py",
                  "hg_average_to_agentbench_compare.py",
                  "hg_average_to_alpacaeval_compare.py",
                  "hg_average_to_mosaic_compare.py",
                  "hg_average_to_mt_bench_compare.py",
                  "hg_average_to_opencompass_compare.py"
                  ]

for script in scripts_to_run:
    run_script(script, True, global_config)