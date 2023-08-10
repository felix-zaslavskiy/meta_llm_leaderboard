import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the data
df = pd.read_csv('../temp_data/hf_llm_data.csv')

# Find the best model within each size_type
best_models = df.loc[df.groupby("size_type")["Average"].idxmax()]

# Define the order for the size_type
# can put back 20B , 40B or 16B in the future, remove 6B
order = [ '70B', '65B', '30B', '13B', '7B', '6B', '3B', '1B']

# Convert the size_type to a category type with the defined order
best_models['size_type'] = pd.Categorical(best_models['size_type'], categories=order, ordered=True)

# Drop rows where 'size_type' is NaN
best_models = best_models.dropna(subset=['size_type'])

# Sort the DataFrame according to the new order
best_models = best_models.sort_values('size_type')

label_offset = 5

# Create the plot with the updated order for horizontal bars
plt.figure(figsize=(8, 8))

sns.set_theme(style='whitegrid')
barplot = sns.barplot(x="Average", y="size_type", data=best_models, color="royalblue", edgecolor='black')

plt.ylabel('Model Size Categories', fontsize=12)
plt.xlabel('Average Rating', fontsize=12)
plt.title('Hugging Face LLM Leaderboard by Model Size', fontweight='bold')

# Annotate the model names on the bars in horizontal orientation
for i in range(best_models.shape[0]):
    model_name = best_models.Model.iloc[i]
    font_size=16
    if len(model_name) > best_models.Average.iloc[i] * 0.7:
        slash_index = model_name.find('/')
        name_length = len(model_name) - slash_index + 1
        model_name = '...' + model_name[slash_index:]
        offset = 22
        if name_length > offset:
            dot_dot = '...'
        else:
            dot_dot = ''
        model_name = model_name[:offset] + dot_dot

    # Use the constant label_offset for the x position
    plt.text(label_offset,  # Aligned to the left of each bar
             i,
             model_name,
             ha='left',  # Left-align the text
             va='center',
             rotation=0,
             fontsize=font_size,
             fontweight='bold',
             color='white')

# Add current date to the top right corner
current_date = datetime.today().strftime('%Y-%m-%d')
plt.text(0.95, 0.95, current_date, fontsize=12, transform=plt.gcf().transFigure, horizontalalignment='right', verticalalignment='top')
plt.text(0.05, 0.95, "@FZaslavskiy", fontsize=12, transform=plt.gcf().transFigure, verticalalignment='top')

plt.tight_layout()
plt.show()
