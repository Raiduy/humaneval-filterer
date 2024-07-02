import json
import pandas as pd
import re
import os

def extract_details(jsonl_file):
    with open(jsonl_file, 'r') as f:
        df = pd.DataFrame()
        for line in f:
            data = json.loads(line)
            task_id = int(data['task_id'].split('/')[1])
            entry_points = data['entry_point']
            prompt = data['prompt']
            df_line = pd.DataFrame({'ID': [task_id], 'Name': [entry_points], 'Description': [prompt]})
            df = pd.concat([df, df_line])
        return df
    
def extract_difficulty(difficulty_file):
    with open(difficulty_file, 'r') as f:
        df = pd.DataFrame()
        for line in f:
            task_id = int(line.split('_')[0])
            difficulty = re.findall(r"(\d+)(?!.*\d)", line)[0]
            df_line = pd.DataFrame({'ID': [task_id], 'LLM Solved Count': [difficulty]})
            df = pd.concat([df, df_line])
        return df

if __name__ == '__main__':
    df = extract_details('./data/human-eval-v2-20210705.jsonl')
    df_difficulty = extract_difficulty('./first_analysis/difficulty.txt')
    df = pd.merge(df, df_difficulty, on='ID', how='left')
    df.to_excel('./first_analysis/details.xlsx', index=False)
