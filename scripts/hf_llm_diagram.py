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
#best_models['size_type'] = best_models['size_type'].astype(str)

# Drop rows where 'size_type' is NaN
best_models = best_models.dropna(subset=['size_type'])

# Sort the DataFrame according to the new order
best_models = best_models.sort_values('size_type')

# Create the plot with the updated order
plt.figure(figsize=(10, 8))

sns.set_theme(style='whitegrid')
#sns.set(style='whitegrid', palette='pastel', context='talk', font='Arial', font_scale=1.2)
barplot = sns.barplot(x="size_type", y="Average", data=best_models, color="royalblue", edgecolor='black')

plt.xlabel('Model Size Categories', fontsize=12)
plt.ylabel('Average Rating', fontsize=12)
plt.title('Hugging Face LLM Leaderboard by Model Size', fontweight='bold')

# Annotate the model names on the bars in vertical orientation
for i in range(best_models.shape[0]):
    model_name = best_models.Model.iloc[i]
    font_size=16
    # Append "(pretrained)" to the model name if its type is "pretrained"
    #if best_models.Type.iloc[i] == 'pretrained':
    #    model_name += ' (pretrained only)'
    # Truncate the model name if it's longer than the bar height
    #print(len(model_name))
    #print(best_models.Average.iloc[i])
    if len(model_name) > best_models.Average.iloc[i] * 0.7:
        slash_index = model_name.find('/')
        name_length = len(model_name) - slash_index + 1
        model_name = '...' + model_name[slash_index:]
        offset = 22
        if name_length > offset:
            dot_dot = '...'
        else:
            dot_dot = ''
        model_name = model_name[:offset]  + dot_dot

    plt.text(i,
             best_models.Average.iloc[i]/2,  # Position at half height for better visibility
             model_name,
             ha = 'center',
             va = 'center',
             rotation='vertical',
             fontsize=font_size,  # Increase font size
             fontweight='bold',  # Make font bolder
             color='white')  # Change font color for better visibility

# Add current date to the top right corner
current_date = datetime.today().strftime('%Y-%m-%d')
plt.text(0.95, 0.95, current_date, fontsize=12, transform=plt.gcf().transFigure, horizontalalignment='right', verticalalignment='top')
plt.text(0.05, 0.95, "@FZaslavskiy", fontsize=12, transform=plt.gcf().transFigure, verticalalignment='top')

plt.tight_layout()
plt.show()
