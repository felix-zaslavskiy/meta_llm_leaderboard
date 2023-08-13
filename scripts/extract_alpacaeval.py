
import pandas as pd
from change_tracker import load_previous_data, save_current_data, track_changes
# Load the data
url = "https://github.com/tatsu-lab/alpaca_eval/raw/main/docs/alpaca_eval_gpt4_leaderboard.csv"
df = pd.read_csv(url)

# Filter rows where Link starts with "https://huggingface.co/" or the specific arXiv link
df = df[df['link'].str.startswith("https://huggingface.co/") |
        (df['link'] == "https://ai.meta.com/llama/") |
        (df['link'] == "https://github.com/imoneoi/openchat")]

# Extract the Model_ID from the Link column, with special handling for the arXiv link
def extract_model_id(link, name):
    if link == "https://ai.meta.com/llama/" and name == 'LLaMA2 Chat 70B':
        return "meta-llama/Llama-2-70b-chat-hf"
    elif link == "https://ai.meta.com/llama/" and name == 'LLaMA2 Chat 13B':
        return "meta-llama/Llama-2-13b-chat-hf"
    elif link == "https://ai.meta.com/llama/" and name == 'LLaMA2 Chat 7B':
        return "meta-llama/Llama-2-13b-chat-hf"
    elif link == "https://github.com/imoneoi/openchat" and name == 'OpenChat V3.1 13B':
        return "openchat/openchat_v3.1"
    elif link == "https://github.com/imoneoi/openchat" and name == 'OpenChat V2-W 13B':
        return "openchat/openchat_v2_w"
    elif link == "https://github.com/imoneoi/openchat" and name == 'OpenChat V2 13B':
        return "openchat/openchat_v2"
    elif link == "https://github.com/imoneoi/openchat" and name == 'OpenChat-13B':
        return "openchat/openchat"
    elif link == "https://github.com/imoneoi/openchat" and name == 'OpenChat8192-13B':
        return "oopenchat/openchat_8192"
    elif link == "https://github.com/imoneoi/openchat" and name == 'OpenCoderPlus-15B':
        return "openchat/opencoderplus"
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