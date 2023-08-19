import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from save_chart import display_or_save
import argparse

parser = argparse.ArgumentParser(description="Your script description")
parser.add_argument('--save_to_file', action='store_true')
# Parse the arguments
args = parser.parse_args()
save_to_file = args.save_to_file

# Load the merged CSV file
file_path = "../temp_data/hf_llm_data_merged_mosaic.csv"
merged_data = pd.read_csv(file_path)

# Filter out rows with empty or NaN values in the "Mosaic_Avg" column
filtered_data = merged_data.dropna(subset=['Mosaic_Avg'])

# Scale the "MT-bench" values by 10 for better visualization
filtered_data['Mosaic_Avg'] *= 70

# Set plot size with increased width for better visibility of model names
plt.figure(figsize=(15, 8))

# Create a horizontal bar plot for "HF LLM Average" and "MT-bench" values per "Model"
sns.barplot(x="Average", y="Model", data=filtered_data, color="skyblue", label="HF LLM Average")
sns.barplot(x="Mosaic_Avg", y="Model", data=filtered_data, color="red", label="Mosaic_Avg (scaled by 70)")

# Add legend
plt.legend(loc='lower right')

# Add labels and title
plt.xlabel('Score', fontsize=12)
plt.ylabel('Model', fontsize=12)
plt.title('Comparison of HF LLM Average and Mosaic Avg Scores by Model', fontsize=14)

# Use tight_layout to ensure that everything fits within the figure bounds
plt.tight_layout()

display_or_save(plt, save_to_file)
