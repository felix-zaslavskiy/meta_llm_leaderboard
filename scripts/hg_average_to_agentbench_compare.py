import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from save_chart import display_or_save
import argparse
import json

parser = argparse.ArgumentParser(description="Your script description")
parser.add_argument('--save_to_file', action='store_true')
parser.add_argument("--global_config", type=str, help="JSON string containing global configurations.")

# Parse the arguments
args = parser.parse_args()
# If global_config argument is passed, parse it
if args.global_config:
    global_config = json.loads(args.global_config)
else:
    global_config = {}
save_to_file = args.save_to_file

# Load the merged CSV file
file_path = "../temp_data/hf_llm_data_merged_agentbench.csv"
merged_data = pd.read_csv(file_path)

# Group by 'Model' and get the row with the max 'Average' for each group
filtered_data = merged_data.loc[merged_data.groupby('Model')['Average'].idxmax()]

# Sort by 'Average' in descending order
filtered_data = filtered_data.sort_values(by="Average", ascending=False)

# Filter out rows with empty or NaN values in the "MT-bench" column
filtered_data = filtered_data.dropna(subset=['AgentBench'])

# Scale the "MT-bench" values by 3 for better visualization
filtered_data['AgentBench'] *= 30

# Set plot size with increased width for better visibility of model names
plt.figure(figsize=(15, 8))

# Create a horizontal bar plot for "HF LLM Average" and "MT-bench" values per "Model"
sns.barplot(x="Average", y="Model", data=filtered_data, color="skyblue", label="HF LLM Average")
sns.barplot(x="AgentBench", y="Model", data=filtered_data, color="red", label="AgentBench (scaled by 30)")

# Truncate y-axis labels if they are too long
y_labels = [label.get_text() if len(label.get_text()) <= 36 else '...' + label.get_text()[-36:] for label in plt.gca().get_yticklabels()]
plt.gca().set_yticklabels(y_labels)

# Add legend
plt.legend(loc='lower right')

# Add labels and title
plt.xlabel('Score', fontsize=12)
plt.ylabel('Model', fontsize=12)
plt.title('Comparison of HF LLM Average and AgentBench Scores by Model', fontsize=14)

plt.text(0.05, 0.95, global_config.get("CHART_TAG"), fontsize=12, transform=plt.gcf().transFigure, verticalalignment='top')

# Use tight_layout to ensure that everything fits within the figure bounds
plt.tight_layout()

display_or_save(plt, save_to_file, global_config.get("DATETIME"))
