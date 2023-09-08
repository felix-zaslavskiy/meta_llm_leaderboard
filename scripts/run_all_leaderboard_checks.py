import subprocess
import sys
def run_script(script_name, specific_exit_code=2):
    result = subprocess.run(["python", script_name])
    if result.returncode == specific_exit_code:
        return script_name
    elif result.returncode != 0:
        print(f"Script {script_name} failed with error code {result.returncode}\n")
        sys.exit(0)
    else:
        print(f"Script {script_name} executed successfully!\n")
        return None

scripts_to_run = ["hf_llm_leaderboard.py",
                  "extract_alpacaeval.py",
                  "extract_lmsys.py",
                  "scrape_mosaicml_leaderboard.py",
                  "scrape_opencompass_leaderboard.py",
                  "extract_bigcode.py"]


next_script = {
    "extract_alpacaeval.py": ["merge_llm_to_alpacaeval.py", "hg_average_to_alpacaeval_compare.py"],
    "extract_lmsys.py": ["merge_llm_to_lmsys.py", "hg_average_to_mt_bench_compare.py"],
    "scrape_mosaicml_leaderboard.py": ["merge_llm_to_mosaic.py", "hg_average_to_mosaic_compare.py"],
    "scrape_opencompass_leaderboard.py": ["merge_llm_to_opencompass.py", "hg_average_to_opencompass_compare.py"],
}

for script in scripts_to_run:
    result = run_script(script)
    if result:
        print(f'running follow up scripts for {script}')
        # Run the subsequent scripts for the main script
        for subsequent_script in next_script.get(script, []):
            run_script(subsequent_script)




