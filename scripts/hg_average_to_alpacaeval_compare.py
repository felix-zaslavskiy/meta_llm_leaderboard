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

sorted_data = filtered_data.sort_values(by='win_rate', ascending=False)

# Melt the DataFrame to have a "method" column and a "score" column
melted_data = pd.melt(sorted_data, id_vars="Model", value_vars=["Average", "win_rate"],
                      var_name="Method", value_name="Score")

# Map the method names to more descriptive labels
melted_data["Method"] = melted_data["Method"].map({"Average": "HF LLM Average", "win_rate": "AlpacaEval_WinRate"})

# Create the side-by-side barplot using the hue parameter
plt.figure(figsize=(15, 8))
sns.barplot(x="Score", y="Model", hue="Method", data=melted_data, palette=["skyblue", "red"])

plt.legend(handles=[plt.Line2D([0], [0], color='skyblue', lw=4, label='HF LLM Average'),
                    plt.Line2D([0], [0], color='red', lw=4, label='AlpacaEval_WinRate')],
           loc='lower right')

#plt.grid(False)  # Turn off grid
# Add labels and title
plt.xlabel('Score', fontsize=12)
plt.ylabel('Model', fontsize=12)
plt.title('Comparison of HF LLM Average and AlpacaEval win rate by Model', fontsize=14)

# Use tight_layout to ensure that everything fits within the figure bounds
plt.tight_layout()

plt.show()