from gradio_client import Client
import json
import csv
from models import Model
from change_tracker import load_previous_data, save_current_data, track_changes

# Param to initialize the model list json in temp data folder. Only needed on demand.
create_init_list = False

client = Client("https://huggingfaceh4-open-llm-leaderboard.hf.space/")

job = client.submit(fn_index=6)
json_data = job.result(timeout=120)


with open(json_data[0], 'r') as file:
    file_data = file.read()

# Load the JSON data
data = json.loads(file_data)

# Get the headers and the data
headers = data['headers']
data = data['data']

def categorize_size(params, name):

    model = Model.find_by_hf_id("../static_data/models.json", name)
    if model is None:
        if params == 0.0:
            return 'other'
        elif params <= 2.0:
            return "1B"
        elif params <= 4.0:
            return "3B"
        elif params <= 6.5:
            return "6B"
        elif params <= 8.0:
            return "7B"
        elif params <= 13.5:
            return "13B"
        elif params <= 17.0:
            return "16B"
        elif params <= 25.0:
            return "20B"
        elif params <= 35.0:
            return "30B"
        elif params <= 45.0:
            return "40B"
        elif params <= 66.0:
            return "65B"
        elif params <= 75.0:
            return "70B"
        elif params <= 190.0:
            return "180B"
        else:
            raise Exception("Param too big")
    else:
        return model.SIZE


# Create a new dictionary with model->status
model_status_dict = {}
init_list = []
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

        model_name_key = d['model_name_for_query']
        # We could have multiple evaluations with same key
        d['Model'] = model_name_key
        # Make key unique
        model_name_key = model_name_key + "_" + d['Precision'] + '_' + d['Model sha']
        del d['model_name_for_query']
        del d['Model sha']
        del d['T']
        num_param = 0.0 if d['#Params (B)'] == None else float(d['#Params (B)'])

        d['size_type'] = categorize_size(num_param, d['Model'])

        # Add the model name and status to the dictionary
        model_status_dict[model_name_key] = d['Average']

        w.writerow(d)

        if create_init_list:
            init_list.append(Model(ID=d['Model'],
                                HF_ID=d['Model'],
                                URL="https://huggingface.co/" + d['Model'],
                                SIZE=d['size_type'],
                                LICENSE=d['Hub License']))

if create_init_list:
    Model.save_to_file(init_list, '../temp_data/hf_model_list.json')

previous_data = load_previous_data('../temp_data/hf_leaderboard_state.dat')
save_current_data(model_status_dict, '../temp_data/hf_leaderboard_state.dat')
track_changes(model_status_dict, previous_data)
