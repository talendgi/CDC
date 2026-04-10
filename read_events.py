import pandas as pd

df = pd.read_json("cdc_output.json", lines=True)
print(df.head())