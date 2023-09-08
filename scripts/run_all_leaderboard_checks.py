import subprocess

def run_script(script_name):
    result = subprocess.run(["python", script_name])
    if result.returncode != 0:
        print(f"Script {script_name} failed with error code {result.returncode}\n")
        # Handle error (e.g., exit or move to the next script)
    else:
        print(f"Script {script_name} executed successfully!\n")

scripts_to_run = ["extract_alpacaeval.py",
                  "extract_lmsys.py",
                  "hf_llm_leaderboard.py",
                  "scrape_mosaicml_leaderboard.py",
                  "scrape_opencompass_leaderboard.py",
                  "extract_bigcode.py"]

for script in scripts_to_run:
    run_script(script)