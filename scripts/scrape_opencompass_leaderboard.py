import requests
import json
import pandas as pd

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

# Prepare an empty list to hold the processed data
processed_data = []

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

        # Append this data to the processed_data list
        processed_data.append([model_name, Model_ID, average, size])

# Convert the processed data to a DataFrame
df = pd.DataFrame(processed_data, columns=['model_name', 'Model_ID', 'average', 'size'])

# Save the DataFrame to a CSV file
df.to_csv('../temp_data/opencompass_data.csv', index=False)