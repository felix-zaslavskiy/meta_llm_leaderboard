import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib.lines import Line2D
from models import Model
from save_chart import display_or_save
import argparse
import json

# Make a chart of the models from HF leaderboard based on size category.

# Set up the argument parser
parser = argparse.ArgumentParser(description="Your script description")
parser.add_argument('--license', type=str, choices=['all', 'other_permissive', 'permissive'], default='all', help="Which models to show")
parser.add_argument('--rescore', action='store_true', help="Set rescore to True")
parser.add_argument('--rescore2', action='store_true', help="Set rescore2 to True")
parser.add_argument('--save_to_file', action='store_true')
parser.add_argument("--global_config", type=str, help="JSON string containing global configurations.")

# Parse the arguments
args = parser.parse_args()

# If global_config argument is passed, parse it
if args.global_config:
    global_config = json.loads(args.global_config)
else:
    global_config = {}

# Set the variable based on the presence of --rescore
rescore = args.rescore
rescore2 = args.rescore2
save_to_file = args.save_to_file
show_license = args.license

# Load the data
df = pd.read_csv('../temp_data/hf_llm_data.csv')

# Define a function to check if a model is contaminated
def is_contaminated_or_no_info(model_id):
    model = Model.find_by_hf_id("../static_data/models.json", model_id)
    if model and ( model.CONTAMINATED or model.HAS_NO_MODEL_CARD ):
        return True
    return False

# Create a mask indicating whether each row is contaminated
contaminated_mask = df['Model'].apply(is_contaminated_or_no_info)

# Use the mask to filter out contaminated rows
filtered_df = df[~contaminated_mask]
df = filtered_df

if rescore == True:
    df['Average'] = df['ARC'] * 0.3 + df['HellaSwag'] * 0.3 + df['MMLU'] * 0.3 + df['TruthfulQA'] * 0.1

if rescore2 == True:
    df['Average'] = df['ARC'] * 0.5 + df['MMLU'] * 0.5

def strip_brackets(license_str):
    # Check if the input is a string
    if not isinstance(license_str, str):
        return license_str
    # If the string starts with '[' and ends with ']', strip them
    if license_str.startswith('[\'') and license_str.endswith('\']'):
        return license_str[2:-2]
    return license_str

# Non-Commercial (blue - can't use commercially)
# Commercial - commercially permissible.
# Other - Unknown.
def commercial_permissible(license):
    license = strip_brackets(license)
    match license:
        case 'agpl-3.0':
            return 'commercial'
        case 'apache-2.0':
            return 'commercial'
        case 'bigcode-openrail-m':
            return "commercial"
        case 'bigscience-openrail-m':
            return "commercial"
        case 'bigscience-bloom-rail-1.0':
            return "commercial"
        case 'bsd-3-clause':
            return "commercial"
        case 'cc':
            return "commercial"
        case 'cc0-1.0':
            return "non-commercial"
        case 'cc-by-nc-4.0':
            return "non-commercial"
        case 'cc-by-nc-nd-4.0':
            return "non-commercial"
        case 'cc-by-nc-sa-4.0':
            return "non-commercial"
        case 'creativeml-openrail-m':
            return "commercial"
        case 'falcon-180b-license':
            return 'commercial'
        case 'gpl':
            return "commercial"
        case 'gpl-3.0':
            return "commercial"
        case 'llama1':
            return "non-commercial"
        case 'llama2':
            return 'commercial'
        case 'mit':
            return 'commercial'
        case 'openrail':
            return "commercial"
        case 'openrail++':
            return "commercial"
        case 'other':
            return 'other'
        case 'StableBeluga':
            return "non-commercial"
    return ""

# If the license is empty string we want to check in Models registry.
def get_license_from_registry(row):
    if row['license_type'] == '' or row['license_type'] == 'other':
        model = Model.find_by_hf_id("../static_data/models.json", row['Model'])
        if model is None:
            return 'other'
        else:
            return commercial_permissible(model.LICENSE)
    return row['license_type']

# Apply license type calculation on the Hug license
df['license_type'] = df['Hub License'].apply(commercial_permissible)

# Fill in or override license based on model registry
df['license_type'] = df.apply(get_license_from_registry, axis=1)

if show_license == 'other_permissive':
    df_filtered = df[df['license_type'].isin(['commercial']) | df['license_type'].isin(['other'])]
    df = df_filtered
elif show_license == 'permissive':
    df_filtered =  df[df['license_type'].isin(['commercial'])]
    df = df_filtered

# Find the best model within each size_type
best_models = df.loc[df.groupby("size_type")["Average"].idxmax()]

# Define the order for the size_type
# can put back 20B , 40B or 16B in the future, remove 6B
order = [ '180B', '70B', '30B', '13B', '7B', '6B', '3B', '1B']


# Convert the size_type to a category type with the defined order
best_models['size_type'] = pd.Categorical(best_models['size_type'], categories=order, ordered=True)

# Drop rows where 'size_type' is NaN
best_models = best_models.dropna(subset=['size_type'])

# Sort the DataFrame according to the new order
best_models = best_models.sort_values('size_type')


label_offset = 5

max_average = best_models["Average"].max()
label_offset_license = max_average + 0.045 * max_average  # adds a 2% buffer to the right of the longest bar

# Create the plot with the updated order for horizontal bars
plt.figure(figsize=(8, 8))

sns.set_theme(style='whitegrid')

license_colors_mapping = {
    'non-commercial': 'royalblue',
    'commercial': 'green',
    'other': 'orange'
}

license_colors = {
    "NC": "royalblue",
    "CP": "green",
    "O": "orange"
}
colors_list = best_models['license_type'].apply(lambda x: license_colors_mapping.get(x, 'royalblue')).tolist()

barplot = sns.barplot(x="Average", y="size_type", data=best_models, palette=colors_list, color="royalblue", edgecolor='black')

# Create custom legend handles
legend_elements = [Line2D([0], [0], color='white', markerfacecolor=license_colors["CP"], marker='s', markersize=8, label='CP - Commercially Permissible'),
                   Line2D([0], [0], color='white', markerfacecolor=license_colors["NC"], marker='s', markersize=8, label='NC - Non-Commercial'),
                   Line2D([0], [0], color='white', markerfacecolor=license_colors["O"], marker='s', markersize=8, label='O - Other or Unknown')]


# Add the legend to the plot
plt.legend(handles=legend_elements, loc='lower right', title='Licenses')

if rescore:
    title_text = 'Hugging Face LLM Leaderboard **RESCORED**'
    xlabel_text= 'Average Rating (TruthfulQA = 10%, from original 25% )'
elif rescore2:
    title_text = 'Hugging Face LLM Leaderboard **RESCORED** (2)'
    xlabel_text= 'Average Rating (ARC = 50%, MMLU = 50%)'
else:
    title_text = 'Hugging Face LLM Leaderboard by Model Size'
    xlabel_text= 'Average Rating'

plt.ylabel('Model Size Categories', fontsize=12)
plt.xlabel(xlabel_text, fontsize=12)
# Before plotting, set the default font
plt.text(0.5, 0.95, title_text, fontweight='bold', fontsize=14, transform=plt.gcf().transFigure, horizontalalignment='center', verticalalignment='top')

# Annotate the model names on the bars in horizontal orientation
# Annotate the model names on the bars in horizontal orientation
model_id_list = []
for i, row in best_models.iterrows():
    model_name = row['Model']
    model_id_list.append(model_name)
    size_type = row['size_type']
    y_position = order.index(size_type)  # Get the index from the order list
    font_size = 16
    license_type = row['license_type']
    license_type_display = ''
    if license_type == 'commercial':
        license_type_display = 'CP'
    elif license_type == 'non-commercial':
        license_type_display = 'NC'
    else:
        license_type_display = 'O'

    if len(model_name) > row['Average'] * 0.7:
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
             y_position,  # Use y_position instead of i
             model_name,
             ha='left',  # Left-align the text
             va='center',
             rotation=0,
             fontsize=font_size,
             fontweight='bold',
             color='white')

    plt.text(label_offset_license,
             y_position,  # Use y_position instead of i
             license_type_display,
             rotation=0,
             fontsize=12,
             color='black',
             fontweight='bold',
             ha='right')


# Add current date to the top right corner
current_date = datetime.today().strftime('%Y-%m-%d')
plt.text(0.95, 0.95, current_date, fontsize=12, transform=plt.gcf().transFigure, horizontalalignment='right', verticalalignment='top')
plt.text(0.05, 0.95, global_config.get("CHART_TAG"), fontsize=12, transform=plt.gcf().transFigure, verticalalignment='top')

# Check for missing data in each size_type and annotate
for i, size in enumerate(order):
    if size not in best_models['size_type'].values:
        plt.text(5,  # This will place the text at the start of where the bar would be
                 i,  # This will place the text at the correct y position
                 "No model at this size",
                 ha='left',
                 va='center',
                 rotation=0,
                 fontsize=14,
                 color='grey')  # You can adjust the color as needed

plt.tight_layout()

postfix = None
if rescore:
    postfix = 'rescore'
elif rescore2:
    postfix = 'rescore2'
elif show_license != 'all':
    postfix = show_license

display_or_save(plt, save_to_file, global_config.get("DATETIME"), postfix, model_id_list=model_id_list)