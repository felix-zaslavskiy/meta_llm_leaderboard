import pandas as pd
from change_tracker import load_previous_data, save_current_data, track_changes
from models import Model

url = "https://huggingface.co/spaces/bigcode/bigcode-models-leaderboard/raw/main/data/code_eval_board.csv"
df = pd.read_csv(url)

def extract_model_id(link, name):
    if not link.startswith("https://huggingface.co/"):
        model = Model.find_by_alias("../static_data/models.json", name)
        if model is None:
            return 'other'
        else:
            return model.HF_ID
    else:
        return link.replace("https://huggingface.co/", "")

df['Model_ID'] = df.apply(lambda row: extract_model_id(row['Links'], row['Models']), axis=1)

# Extract the "MT-bench (score)" column and Model_ID
result = df[['Model_ID', 'Win Rate']]

# Print or use the result as needed
#print(result)

# Save to CSV file
file_path = "../temp_data/code_eval_data.csv"
result.to_csv(file_path, index=False)

model_status_dict = df.set_index('Model_ID')['Win Rate'].to_dict()

previous_data = load_previous_data('../temp_data/code_eval_leaderboard_state.dat')
save_current_data(model_status_dict, '../temp_data/code_eval_leaderboard_state.dat')
track_changes(model_status_dict, previous_data)