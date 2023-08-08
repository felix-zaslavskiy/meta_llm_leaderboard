import pickle
import os
from gradio_client import Client
import json
import csv


client = Client("https://huggingfaceh4-open-llm-leaderboard.hf.space/")

json_data = client.predict(
    fn_index=4)

#json_data = client.predict(
#    "null",	# str representing filepath to JSON file in 'parameter_13' Dataframe component
#    "null",	# str representing filepath to JSON file in 'parameter_12' Dataframe component
#    "all",
#    fn_index=2)

with open(json_data[0], 'r') as file:
    file_data = file.read()

# Load the JSON data
data = json.loads(file_data)

# Get the headers and the data
headers = data['headers']
data = data['data']

def categorize_size(params, name):
    if params == 0.0:
        if name == 'stabilityai/FreeWilly2':
            return "70B"
        elif name == 'stabilityai/StableBeluga2':
            return "70B"
        return "other"
    elif params <= 1.0:
        return "1B"
    elif params <= 3.0:
        return "3B"
    elif params <= 6.0:
        return "6B"
    elif params <= 7.5:
        return "7B"
    elif params <= 13.5:
        return "13B"
    elif params <= 16.5:
        return "16B"
    elif params <= 20.5:
        return "20B"
    elif params <= 35.0:
        return "30B"
    elif params <= 45.0:
        return "40B"
    elif params <= 66.0:
        return "65B"
    elif params <= 75.0:
        return "70B"
    else:
        raise Exception("Param too big")

# Create a new dictionary with model->status
model_status_dict = {}

with open('../temp_data/hf_llm_data.csv', 'w', newline='') as f:
    headers_clean = []

    for value in headers:
        text = value.replace('\u2b06\ufe0f', '')
        text = text.replace('\u2764\uFE0F', '').rstrip()
        headers_clean.append(text)

    # Create a dictionary from the headers and the data
    data_dict = [dict(zip(headers_clean, d)) for d in data]

    headers_clean.pop()
    headers_clean.pop()
    headers_clean.append('size_type')
    w = csv.DictWriter(f, headers_clean)
    w.writeheader()

    for d in data_dict:
        # Parse the HTML to get the model name
        #soup = BeautifulSoup(d['Model'], 'html.parser')
        if d['Model'] == '<p>Baseline</p>':
            continue

        model_name = d['model_name_for_query']
        d['Model'] = model_name
        del d['model_name_for_query']
        del d['Model sha']
        del d['T']
        num_param = 0.0 if d['#Params (B)'] == None else float(d['#Params (B)'])

        d['size_type'] = categorize_size(num_param, d['Model'])

        # Add the model name and status to the dictionary
        model_status_dict[model_name] = d['Average']

        w.writerow(d)


# Load the previous data if it exists
if os.path.exists('../temp_data/hf_leaderboard_state.dat'):
    with open('../temp_data/hf_leaderboard_state.dat', 'rb') as file:
        previous_data = pickle.load(file)
else:
    previous_data = {}

# Save the current data
with open('../temp_data/hf_leaderboard_state.dat', 'wb') as file:
    pickle.dump(model_status_dict, file)

# Compare the previous data with the current data
had_change=False
for key in model_status_dict:
    if key not in previous_data:
        print(f'New model: {key}')
        had_change=True
    elif model_status_dict[key] != previous_data[key]:
        print(f'Model {key} changed from {previous_data[key]} to {model_status_dict[key]}')
        had_change=True

for key in previous_data:
    if key not in model_status_dict:
        print(f'Model {key} was removed')
        had_change=True

if not had_change:
    print("No changes")
