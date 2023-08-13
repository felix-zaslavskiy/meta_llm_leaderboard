import requests
import json
import pandas as pd

from change_tracker import load_previous_data, save_current_data, track_changes

# URL of the JSON data
url = 'https://opencompass.oss-cn-shanghai.aliyuncs.com/assets/large-language-model-data.json'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Load the data into a Python object
    data = json.loads(response.text)
else:
    print(f'Request failed with status code {response.status_code}')
    raise Exception('Unable to get Open compass leaderboard')

# Prepare an empty list to hold the processed data
processed_data = []
model_status_dict = {}
if data:
    # Iterate over each model in the OverallENTable
    for item in data['OverallENTable']:
        # Get the model name
        model_name = item['model']

        # Get the Model_ID from the 'weights' list in the 'models' dictionary
        Model_ID = data['models'][model_name]['weight'][0] if model_name in data['models'] and data['models'][model_name]['weight'] else None

        # Get the average from the 'average' field
        average = item['average']

        # Get the size from the 'num' field
        size = item['num']

        Model_ID = Model_ID if Model_ID else model_name

        model_status_dict[Model_ID] = average

        # Append this data to the processed_data list
        processed_data.append([model_name, Model_ID, average, size])

# Convert the processed data to a DataFrame
df = pd.DataFrame(processed_data, columns=['model_name', 'Model_ID', 'average', 'size'])

# Save the DataFrame to a CSV file
df.to_csv('../temp_data/opencompass_data.csv', index=False)


previous_data = load_previous_data('../temp_data/opencompass_leaderboard_state.dat')
save_current_data(model_status_dict, '../temp_data/opencompass_leaderboard_state.dat')
track_changes(model_status_dict, previous_data)