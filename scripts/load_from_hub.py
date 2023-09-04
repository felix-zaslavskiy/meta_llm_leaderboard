
import pandas as pd
from huggingface_hub import Repository
from transformers import AutoConfig

from scripts.display_models.get_model_metadata import apply_metadata
from scripts.display_models.read_results import get_eval_results_dicts
from scripts.display_models.utils import AutoEvalColumn, has_no_nan_values

baseline = {
    AutoEvalColumn.model.name: "<p>Baseline</p>",
    AutoEvalColumn.revision.name: "N/A",
    AutoEvalColumn.precision.name: None,
    AutoEvalColumn.average.name: 25.0,
    AutoEvalColumn.arc.name: 25.0,
    AutoEvalColumn.hellaswag.name: 25.0,
    AutoEvalColumn.mmlu.name: 25.0,
    AutoEvalColumn.truthfulqa.name: 25.0,
    AutoEvalColumn.dummy.name: "baseline",
    AutoEvalColumn.model_type.name: "",
}

def load_all_info_from_hub(RESULTS_REPO: str, RESULTS_PATH: str) -> Repository:

    print("Pulling evaluation requests and results.")

    eval_results_repo = Repository(
        local_dir=RESULTS_PATH,
        # clone_from=RESULTS_REPO,
        repo_type="dataset",
    )
    # TODO: disable git pull for testing.
    # eval_results_repo.git_pull()

    return eval_results_repo


def get_leaderboard_df(
    eval_results: Repository, eval_results_private: Repository, cols: list, benchmark_cols: list
) -> pd.DataFrame:
    if eval_results:
        print("Pulling evaluation results for the leaderboard.")
        # Disable temporarily
        # eval_results.git_pull()
    if eval_results_private:
        print("Pulling evaluation results for the leaderboard.")
        eval_results_private.git_pull()

    all_data = get_eval_results_dicts()

    all_data.append(baseline)
    apply_metadata(all_data)  # Populate model type based on known hardcoded values in `metadata.py`

    df = pd.DataFrame.from_records(all_data)
    df = df.sort_values(by=[AutoEvalColumn.average.name], ascending=False)
    df = df[cols].round(decimals=2)

    # filter out if any of the benchmarks have not been produced
    df = df[has_no_nan_values(df, benchmark_cols)]
    return df



def is_model_on_hub(model_name: str, revision: str) -> bool:
    try:
        AutoConfig.from_pretrained(model_name, revision=revision, trust_remote_code=False)
        return True, None

    except ValueError:
        return (
            False,
            "needs to be launched with `trust_remote_code=True`. For safety reason, we do not allow these models to be automatically submitted to the leaderboard.",
        )

    except Exception as e:
        print(f"Could not get the model config from the hub.: {e}")
        return False, "was not found on hub!"
