import pandas as pd

# Load the provided Excel file again
df = pd.read_excel("../temp_data/agentbench_leaderboard-230808.xlsx")

df['Model_ID'] = df['Models'] + df['VER'].apply(lambda x: '_' + x if x != '-' else '')

# Save the data to a CSV file
csv_file_path = "../temp_data/agentbench_leaderboard.csv"
df.to_csv(csv_file_path, index=False)

