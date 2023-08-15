import pandas as pd
from scripts.models import Model

# Load the provided Excel file again
df = pd.read_excel("../temp_data/agentbench_leaderboard-230808.xlsx")

df['Model_ID_Temp'] = df['Models'] + df['VER'].apply(lambda x: '_' + x if x != '-' else '')

def get_model_id(row):
    model = Model.find_by_alias("../static_data/models.json", row['Model_ID_Temp'])
    if model is None:
        return ''
    else:
        return model.HF_ID

df['Model_ID'] = df.apply(get_model_id, axis=1)

# Save the data to a CSV file
csv_file_path = "../temp_data/agentbench_leaderboard.csv"
df.to_csv(csv_file_path, index=False)

