import pandas as pd
import json
import os
from pathlib import Path


df = pd.read_csv('../data/manga_data.csv', encoding='latin-1')

def safe_json_loads(json_str):
    try:
        return json.loads((json_str))
    except json.JSONDecodeError:
        print(json_str)
        return []

df['Categories'] = df['Categories'].apply(safe_json_loads)

df = df[df['Categories'].apply(lambda categories: len(categories) > 0)]

output_path = "../data/updated_manga_data.csv"

df.to_csv(output_path, index=False)

