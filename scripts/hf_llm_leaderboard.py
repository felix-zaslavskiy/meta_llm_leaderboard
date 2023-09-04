import csv
from models import Model
from change_tracker import load_previous_data, save_current_data, track_changes
from load_from_hub import load_all_info_from_hub, get_leaderboard_df

from scripts.display_models.utils import (
    AutoEvalColumn,
    fields,
)

# Param to initialize the model list json in temp data folder. Only needed on demand.
create_init_list = False

RESULTS_REPO = "open-llm-leaderboard/results"
EVAL_RESULTS_PATH = "eval-results"

eval_results = load_all_info_from_hub(
     RESULTS_REPO, EVAL_RESULTS_PATH
)
# Column selection
COLS = [c.name for c in fields(AutoEvalColumn) if not c.hidden]
BENCHMARK_COLS = [
    c.name
    for c in [
        AutoEvalColumn.arc,
        AutoEvalColumn.hellaswag,
        AutoEvalColumn.mmlu,
        AutoEvalColumn.truthfulqa,
    ]
]
data = get_leaderboard_df(eval_results, None, COLS, BENCHMARK_COLS)

# Get the headers and the data
headers = list(data)

def categorize_size(params, name):
    if params == 0.0:
        model = Model.find_by_hf_id("../static_data/models.json", name)
        if model is None:
            return 'other'
        else:
            return model.SIZE
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

def clean_headers(value):
    text = value.replace('\u2b06\ufe0f', '')
    text = text.replace('\u2764\uFE0F', '').rstrip()
    return text
# Create a new dictionary with model->status
model_status_dict = {}
init_list = []
with open('../temp_data/hf_llm_data.csv', 'w', newline='') as f:
    headers_clean = []

    for value in headers:
        text = clean_headers(value)
        headers_clean.append(text)

    headers_clean.pop()
    headers_clean.pop()
    headers_clean.append('size_type')
    w = csv.DictWriter(f, headers_clean)
    w.writeheader()

    print(headers_clean)
    for index, row in data.iterrows():
        d = {clean_headers(key): value for key, value in row.to_dict().items()}

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
