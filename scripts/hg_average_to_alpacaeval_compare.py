import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the merged CSV file
file_path = "../temp_data/hf_llm_data_merged_alpacaeval.csv"
merged_data = pd.read_csv(file_path)

# Filter out rows with empty or NaN values in the "Mosaic_Avg" column
filtered_data = merged_data.dropna(subset=['win_rate'])

# Scale the "MT-bench" values by 10 for better visualization
#filtered_data['average'] *= 10

# Set plot size with increased width for better visibility of model names
plt.figure(figsize=(15, 8))

# Create a horizontal bar plot for "HF LLM Average" and "MT-bench" values per "Model"
sns.barplot(x="Average", y="Model", data=filtered_data, color="skyblue", label="HF LLM Average")
sns.barplot(x="win_rate", y="Model", data=filtered_data, color="red", label="AlpacaEval_WinRate")

# Add legend
plt.legend(loc='lower right')

# Add labels and title
plt.xlabel('Score', fontsize=12)
plt.ylabel('Model', fontsize=12)
plt.title('Comparison of HF LLM Average and AlpacaEval win rate by Model', fontsize=14)

# Use tight_layout to ensure that everything fits within the figure bounds
plt.tight_layout()

plt.show()
