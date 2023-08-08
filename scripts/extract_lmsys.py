import pandas as pd

# Load the data
url = "https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard/raw/main/leaderboard_table_20230802.csv"
df = pd.read_csv(url)

# Filter rows where Link starts with "https://huggingface.co/" or the specific arXiv link
df = df[df['Link'].str.startswith("https://huggingface.co/") | (df['Link'] == "https://arxiv.org/abs/2302.13971")]

# Extract the Model_ID from the Link column, with special handling for the arXiv link
def extract_model_id(link):
    if link == "https://arxiv.org/abs/2302.13971":
        return "llama-30b"
    return link.replace("https://huggingface.co/", "")

df['Model_ID'] = df['Link'].apply(extract_model_id)

# Extract the "MT-bench (score)" column and Model_ID
result = df[['Model_ID', 'MT-bench (score)']]

# Print or use the result as needed
print(result)

# Save to CSV file
file_path = "../temp_data/lmsys_data.csv"
result.to_csv(file_path, index=False)
