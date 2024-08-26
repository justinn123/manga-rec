import pandas as pd
import json

df = pd.read_csv('manga_data.csv')

def safe_json_loads(json_str):
    try:
        return json.loads(json_str.replace("'", '"'))
    except json.JSONDecodeError:
        return []
df['Categories'] = df['Categories'].apply(safe_json_loads)

# Step 3: Remove entries with an empty category list
df = df[df['Categories'].apply(lambda categories: len(categories) > 0)]

df.to_csv('manga_data.csv', index=False)


print(df.info())
