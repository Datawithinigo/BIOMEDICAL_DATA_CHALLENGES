import pandas as pd

input_path = "/Users/arriazui/Desktop/master/BIOMEDICAL_DATA_CHALLENGES/Source_data/Unclean data.sav"
output_path = "/Users/arriazui/Desktop/master/BIOMEDICAL_DATA_CHALLENGES/processed_data/output.csv"  # or "output.csv"

df = pd.read_spss(input_path, convert_categoricals=True)
df.to_csv(output_path, index=False)  # or df.to_csv(output_path, index=False)