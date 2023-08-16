
import pandas as pd
from change_tracker import load_previous_data, save_current_data, track_changes
from models import Model

# Load the data
url = "https://github.com/tatsu-lab/alpaca_eval/raw/main/docs/alpaca_eval_gpt4_leaderboard.csv"
df = pd.read_csv(url)

# Filter rows where Link starts with "https://huggingface.co/" or the specific arXiv link
df = df[df['link'].str.startswith("https://huggingface.co/") |
        (df['link'] == "https://ai.meta.com/llama/") |
        (df['link'] == "https://github.com/imoneoi/openchat")]

# Extract the Model_ID from the Link column, with special handling for the arXiv link
def extract_model_id(link, name):
    if not link.startswith("https://huggingface.co/"):
        model = Model.find_by_alias("../static_data/models.json", name)
        if model is None:
            return 'other'
        else:
            return model.HF_ID
    else:
        return link.replace("https://huggingface.co/", "")

df['Model_ID'] = df.apply(lambda row: extract_model_id(row['link'], row['name']), axis=1)

# Extract the "MT-bench (score)" column and Model_ID
result = df[['Model_ID', 'win_rate']]

# Print or use the result as needed
#print(result)

# Save to CSV file
file_path = "../temp_data/alpacaeval_data.csv"
result.to_csv(file_path, index=False)

model_status_dict = df.set_index('Model_ID')['win_rate'].to_dict()

previous_data = load_previous_data('../temp_data/alpacaeval_leaderboard_state.dat')
save_current_data(model_status_dict, '../temp_data/alpacaeval_leaderboard_state.dat')
track_changes(model_status_dict, previous_data)