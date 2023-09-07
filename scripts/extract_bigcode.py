import re

import pandas as pd
from change_tracker import load_previous_data, save_current_data, track_changes
from models import Model
from scripts.utils import get_model_size_cat

url = "https://huggingface.co/spaces/bigcode/multilingual-code-evals/raw/main/data/code_eval_board.csv"
df = pd.read_csv(url)

# Extract the Model_ID from the Link column, with special handling for the arXiv link
def extract_model_id(link, name):
    if pd.isna(link):
        link = ""
    if not link.startswith("https://huggingface.co/"):
        model = Model.find_by_alias("../static_data/models.json", name)
        if model is None:
            return 'other'
        else:
            return model.HF_ID
    else:
        return link.replace("https://huggingface.co/", "")

print(df)
df['Model_ID'] = df.apply(lambda row: extract_model_id(row['Links'], row['Models']), axis=1)

#def categorize_size(params, name):
#    model = Model.find_by_hf_id("../static_data/models.json", name)
#    if model is None:
#        return get_model_size_cat(params)
#    else:
#        return model.SIZE

# May need to use categorize_size if we get a model without size in name
def extract_size_in_billions(name):
    # The regex pattern looks for a number (with optional decimal point)
    # followed by the letter 'b' or 'B'.
    pattern = r'(\d+(\.\d+)?)[bB]'
    match = re.search(pattern, name)
    if match:
        return get_model_size_cat(float(match.group(1)))  # Return the size in billions
    return None

df['size_type'] = df.apply(lambda row: extract_size_in_billions(row['Model_ID']), axis =1)

result = df[['Model_ID', 'Win Rate', 'size_type']]

# Save to CSV file
file_path = "../temp_data/bigcode_data.csv"
result.to_csv(file_path, index=False)

model_status_dict = df.set_index('Model_ID')['Win Rate'].to_dict()

previous_data = load_previous_data('../temp_data/bigcode_leaderboard_state.dat')
save_current_data(model_status_dict, '../temp_data/bigcode_leaderboard_state.dat')
track_changes(model_status_dict, previous_data)