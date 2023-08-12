import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib.lines import Line2D

from scripts.models import Model

# Make a chart of the models from HF leaderboard based on size category.

# Load the data
df = pd.read_csv('../temp_data/hf_llm_data.csv')

def commercial_permissible(license):
    match license:
        # Llama1 is not a HF license. Model is under Llama1 rules.
        case 'llama1':
            return "non-commercial"
        # StableBeluga not a HF license
        case 'StableBeluga':
            return "non-commercial"
        case 'cc-by-nc-4.0':
            return "non-commercial"
        case 'cc-by-nc-sa-4.0':
            return "non-commercial"
        case 'other':
            return 'other'
        case 'llama2':
            return 'commercial'
        case 'cc-by-nc-sa-4.0':
            return
        case 'apache-2.0':
            return 'commercial'
        case "['mit']":
            return 'commercial'
        case "mit":
            return 'commercial'
        case "gpl-3.0":
            return "non-commercial"
        case "openrail":
            return "commercial"
        case "bigscience-openrail-m":
            return "commercial"
        case "creativeml-openrail-m":
            return "commercial"
        case "bsd-3-clause":
            return "commercial"
    return ""

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

best_models['license_type'] = best_models['Hub License'].apply(commercial_permissible)

# If the license is empty string we want to check in Models registry.
def get_license_or_check_registry(row):
    if row['license_type'] == '':
        model = Model.find_by_hf_id("../static_data/models.json", row['Model'])
        if model is None:
            return 'other'
        else:
            return commercial_permissible(model.LICENSE)
    return row['license_type']

best_models['license_type'] = best_models.apply(get_license_or_check_registry, axis=1)

label_offset = 5

# Create the plot with the updated order for horizontal bars

plt.figure(figsize=(8, 8))
plt.rcParams['font.family'] = 'DejaVu Sans'


sns.set_theme(style='whitegrid')
barplot = sns.barplot(x="Average", y="size_type", data=best_models, color="royalblue", edgecolor='black')

# Create custom legend handles
legend_elements = [Line2D([0], [0], color='white', markerfacecolor='black', marker='o', markersize=10, label='CP - Commercially Permissible'),
                   Line2D([0], [0], color='white', markerfacecolor='black', marker='o', markersize=10, label='NC - Non-Commercial'),
                   Line2D([0], [0], color='white', markerfacecolor='black', marker='o', markersize=10, label='O - Other or Unknown')]

# Add the legend to the plot
plt.legend(handles=legend_elements, loc='lower right', title='Licenses')

plt.ylabel('Model Size Categories', fontsize=12)
plt.xlabel('Average Rating', fontsize=12)
# Before plotting, set the default font
#  Does not work yet plt.rcParams['font.family'] = 'Segoe UI Emoji'
#plt.title('🤗Hugging Face LLM Leaderboard🤗 by Model Size', fontweight='bold')
plt.title('Hugging Face LLM Leaderboard by Model Size', fontweight='bold')
# Annotate the model names on the bars in horizontal orientation
for i in range(best_models.shape[0]):
    model_name = best_models.Model.iloc[i]
    font_size=16
    license_type = best_models.license_type.iloc[i]
    license_type_display = ''
    if license_type == 'commercial':
        license_type_display='[CP]'
    elif license_type == 'non-commercial':
        license_type_display='[NC]'
    else:
        license_type_display = '[O]'

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

    model_name += ' ' + license_type_display

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
