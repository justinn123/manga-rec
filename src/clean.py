import pandas as pd
import json
import os
from pathlib import Path


df = pd.read_csv('../data/manga_data.csv', encoding='latin-1')

def safe_json_loads(json_str):
    if pd.isna(json_str) or json_str.strip() == "":
        return []
    try:
        return json.loads((json_str))
    except json.JSONDecodeError:
        print(f"Failed to decode JSON: {json_str}")
        return []

df['Categories'] = df['Categories'].apply(safe_json_loads)
df['Genres'] = df['Genres'].apply(safe_json_loads)


df = df[(df['Title'].notna() & df['Title'].str.strip() != "") & 
        (df['Categories'].apply(lambda categories: len(categories) > 0)) & 
        (df['Genres'].apply(lambda genres: len(genres) > 0)) & 
        (df['Total Category Score'] > 0) & 
        (df['Rating'] >= 1) & (df['Rating'] <= 10)
]


output_path = "../data/updated_manga_data.csv"

df.to_csv(output_path, index=False)

