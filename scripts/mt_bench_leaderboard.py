import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from save_chart import display_or_save
import argparse
import json

# Make a chart of the models from HF leaderboard based on size category.

# Set up the argument parser
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
# Load the data
df = pd.read_csv('../temp_data/lmsys_data.csv')

# Find the best model within each size_type
df = df[df['MT-bench (score)'] != "-"]
df['MT-bench (score)'] = pd.to_numeric(df['MT-bench (score)'], errors='coerce')

best_models = df.loc[df.groupby("size_type")["MT-bench (score)"].idxmax()]

order = [ '70B', '30B', '13B', '7B', '6B', '3B', '1B']


# Convert the size_type to a category type with the defined order
best_models['size_type'] = pd.Categorical(best_models['size_type'], categories=order, ordered=True)

# Drop rows where 'size_type' is NaN
best_models = best_models.dropna(subset=['size_type'])

# Sort the DataFrame according to the new order
best_models = best_models.sort_values('size_type')

# Create the plot with the updated order for horizontal bars
plt.figure(figsize=(8, 8))

sns.set_theme(style='whitegrid')
sns.set(rc={"axes.facecolor": "lightgrey", "grid.color": "white"})
barplot = sns.barplot(x="MT-bench (score)", y="size_type", data=best_models,  color="royalblue", edgecolor='black')

title_text = 'MT Bench Leaderboard'
xlabel_text= 'MT-bench (score)'

plt.ylabel('Model Size Categories', fontsize=12)
plt.xlabel(xlabel_text, fontsize=12)
# Before plotting, set the default font
plt.text(0.5, 0.95, title_text, fontweight='bold', fontsize=14, transform=plt.gcf().transFigure, horizontalalignment='center', verticalalignment='top')

label_offset = 0.5
model_id_list = []
for i, row in best_models.iterrows():
    model_name = row['Model_ID']
    model_id_list.append(model_name)
    size_type = row['size_type']
    y_position = order.index(size_type)  # Get the index from the order list
    font_size = 16

    if len(model_name) > row['MT-bench (score)'] * 5:
        slash_index = model_name.find('/')
        name_length = len(model_name) - slash_index + 1
        model_name = '...' + model_name[slash_index:]
        offset = 28
        if name_length > offset:
            dot_dot = '...'
        else:
            dot_dot = ''
        model_name = model_name[:offset] + dot_dot

    # Use the constant label_offset for the x position
    plt.text(label_offset,  # Aligned to the left of each bar
             y_position,  # Use y_position instead of i
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
plt.text(0.05, 0.95, global_config.get("CHART_TAG"), fontsize=12, transform=plt.gcf().transFigure, verticalalignment='top')

plt.tight_layout()


display_or_save(plt, save_to_file, global_config.get("DATETIME"), None, model_id_list=model_id_list)