import pandas as pd

input_path = "/Users/arriazui/Desktop/master/BIOMEDICAL_DATA_CHALLENGES/Source_data/Unclean data.sav"
output_path = "output.xlsx"  # or "output.csv"

df = pd.read_spss(input_path, convert_categoricals=True)
df.to_excel(output_path, index=False)  # or df.to_csv(output_path, index=False)