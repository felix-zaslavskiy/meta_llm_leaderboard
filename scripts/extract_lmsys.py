import pandas as pd
from change_tracker import load_previous_data, save_current_data, track_changes
# Check if we have a new file first
import git
import os
import re
from datetime import datetime
from scripts.models import Model
from scripts.utils import get_model_size_cat

# Clone the repository
repo_url = "https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard"
repo_dir = "./chatbot-arena-leaderboard"
if not os.path.exists(repo_dir):
    git.Repo.clone_from(repo_url, repo_dir)

# List all files in the root directory of the repository
files = os.listdir(repo_dir)

# Delete the repository files after processing
git.rmtree(repo_dir)

# Extract file names that match the pattern "leaderboard_table_YYYYMMDD.csv"
pattern = r"leaderboard_table_(\d{4})(\d{2})(\d{2}).csv"
dates = []
for file in files:
    match = re.match(pattern, file)
    if match:
        year, month, day = match.groups()
        dates.append((int(year), int(month), int(day)))

# Sort the dates and find the most recent date
dates.sort(reverse=True)
most_recent_date = dates[0] if dates else None


if most_recent_date is None:
    raise Exception('Date can not be empty')

most_recent_date_dt = datetime(most_recent_date[0], most_recent_date[1], most_recent_date[2])
most_recent_date_str = most_recent_date_dt.strftime('%Y%m%d')
print("Most recent date is: " + most_recent_date_str)

model_status_dict = { 'date' : most_recent_date_str }
previous_data = load_previous_data('../temp_data/lmsys_leaderboard_state.dat')
save_current_data(model_status_dict, '../temp_data/lmsys_leaderboard_state.dat')
had_changes = track_changes(model_status_dict, previous_data)

had_changes=True
if had_changes:
    # Load the data
    url = f"https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard/raw/main/leaderboard_table_{most_recent_date_str}.csv"
    df = pd.read_csv(url)

    # Filter rows where Link starts with "https://huggingface.co/" or the specific arXiv link
    #df = df[df['Link'].str.startswith("https://huggingface.co/") | (df['Link'] == "https://arxiv.org/abs/2302.13971")]

    # Extract the Model_ID from the Link column, with special handling for the arXiv link
    def extract_model_id(name, link):
        if link == "https://arxiv.org/abs/2302.13971":
            return "llama-30b"
        elif link.startswith("https://huggingface.co/"):
            return link.replace("https://huggingface.co/", "")
        else:
            model =  Model.find_by_id_or_alias("../static_data/models.json", name)
            if model is None:
                return name
            else:
                return model.HF_ID



    df['Model_ID'] = df.apply(lambda row: extract_model_id(row['Model'], row['Link']), axis=1)


    def categorize_size( name):
        model = Model.find_by_id_or_alias("../static_data/models.json", name)
        if model is None:
            return 'other'
        else:
            return model.SIZE

    df['size_type']= df.apply(lambda row: categorize_size(row['Model_ID']), axis=1)


    # Extract the "MT-bench (score)" column and Model_ID
    result = df[['Model_ID', 'MT-bench (score)','Arena Elo rating', 'size_type']]

    # Print or use the result as needed
    print("New date file: " + most_recent_date_str)
    print(result)

    # Save to CSV file
    file_path = "../temp_data/lmsys_data.csv"
    result.to_csv(file_path, index=False)
