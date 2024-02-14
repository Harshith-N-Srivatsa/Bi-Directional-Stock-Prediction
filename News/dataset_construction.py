import pandas as pd
import json
import os
from pandas import json_normalize

def flatten_dict(d):
    flattened_dict = {}
    for key, value in d.items():
        if isinstance(value, dict):
            for k, v in value.items():
                flattened_dict[f"{key}_{k}"] = v
        else:
            flattened_dict[key] = value
    return flattened_dict

def read_json_files(folder_path):
    dfs = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                data = json.load(file)
                flattened_data = flatten_dict(data)
                dfs.append(pd.DataFrame([flattened_data]))
    return pd.concat(dfs, ignore_index=True)

root_folder = '/Users/nikunjphutela/Downloads/News/'

final_df = pd.DataFrame()
for root, dirs, files in os.walk(root_folder):
    for folder in dirs:
        folder_path = os.path.join(root, folder)
        df = read_json_files(folder_path)
        final_df = pd.concat([final_df, df], ignore_index=True)

df.to_csv('/Users/nikunjphutela/Downloads/News/final_dataset_news.csv')
df['organizations'] = df['organizations'].apply(lambda x: json.loads(x))

df_normalized = json_normalize(df['entities_organizations'])
df = pd.concat([df, df_normalized], axis=1).drop('entities_organizations', axis=1)
df.to_csv('/Users/nikunjphutela/Downloads/News/final_dataset_news_exploded.csv')