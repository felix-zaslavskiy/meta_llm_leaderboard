import pandas as pd

# Read the "hf_llm_data.csv" file
llm_data_path = "../temp_data/hf_llm_data.csv"
llm_data = pd.read_csv(llm_data_path)

# Read the "mosaicml_table.csv" file
lmsys_data_path = "../temp_data/bigcode_data.csv"
bigcode_data = pd.read_csv(lmsys_data_path)

# Rename the Model_ID column to Model in the lmsys_data DataFrame
bigcode_data.rename(columns={'Model': 'BigcodeModel'}, inplace=True)

# Rename the Model_ID column to Model in the lmsys_data DataFrame
bigcode_data.rename(columns={'Model_ID': 'Model'}, inplace=True)

# Merge the two DataFrames on the Model column
merged_data = pd.merge(llm_data, bigcode_data, on='Model', how='left')

# Rename "MT-bench (score)" column to "MT-bench"
#merged_data.rename(columns={'mosaic_average': 'Mosaic_Avg'}, inplace=True)

# Save the merged DataFrame to a new CSV file
merged_file_path = "../temp_data/hf_llm_data_merged_bigcode.csv"
merged_data.to_csv(merged_file_path, index=False)