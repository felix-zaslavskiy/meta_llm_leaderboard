# Load the data
import pandas as pd

df = pd.read_csv('../temp_data/hf_llm_data.csv')

# Define a function to check if a model is contaminated

# Group the dataframe by the license column
grouped = df.groupby('Hub License')

# Get all unique values of the license column
unique_licenses = grouped['Hub License'].unique()

print(unique_licenses)

