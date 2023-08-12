import os
import pickle

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage
# top level url https://www.mosaicml.com/llm-evaluation
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSAwA8-DdEgGHlbX1XkP7KoYWQD2HzKDGsID33MypM17FsjVw5YmT4ceUK-ryfH4jL9jBW8u1DTGWuS/pubhtml?gid=648039812&single=true&widget=false&headers=false&chrome=false'
# Send a GET request to the webpage
response = requests.get(url)

# Parse the HTML content with Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the evaluation table (you will need to inspect the HTML to find the correct tags and attributes)
table = soup.find('table', attrs={'class': 'waffle'})  # Replace with actual class or identifier

# Extract the data from the table
data = []
for row in table.find_all('tr'):
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)

del data[:3]
del data[-1]

# remove license column and rest of necessary columns
for row in data:
    del row[1:3]
    del row[2:]

# Create a pandas DataFrame from the extracted data
df = pd.DataFrame(data, columns=['Model_ID', 'Mosaic_Avg'])  # Adjust columns as needed

df['Model_ID'] = df['Model_ID'].replace('llama-30b', 'huggingface/llama-30b')
df['Model_ID'] = df['Model_ID'].replace('falcon-40b', 'tiiuae/falcon-40b')
df['Model_ID'] = df['Model_ID'].replace('falcon-40b-instruct', 'tiiuae/falcon-40b-instruct')
df['Model_ID'] = df['Model_ID'].replace('mpt-30b', 'mosaicml/mpt-30b')

# Save the DataFrame to a CSV file
df.to_csv('../temp_data/mosaicml_table.csv', index=False)

model_status_dict = df.set_index('Model_ID')['Mosaic_Avg'].to_dict()

#  Change tracking
# Load the previous data if it exists
if os.path.exists('../temp_data/mosaicml_leaderboard_state.dat'):
    with open('../temp_data/mosaicml_leaderboard_state.dat', 'rb') as file:
        previous_data = pickle.load(file)
else:
    previous_data = {}

# Save the current data
with open('../temp_data/mosaicml_leaderboard_state.dat', 'wb') as file:
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