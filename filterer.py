import os
import sys
import pandas as pd
import re
import zipfile
from zipfile import ZipFile
import lizard

SOLUTIONS_FOLDER = './solutions'
OUTPUT_FOLDER = './out'
CYCLOMATIC_COMPLEXITY_THRESHOLD = 1

def check_oneliner(code):
    # remove comments
    code = re.sub(r'"""(.*?)"""', '', code, flags=re.DOTALL)
    code = re.sub(r'#.*', '', code)

    # remove empty lines
    code = '\n'.join([line for line in code.split('\n') if line.strip() != ''])

    for index, line in enumerate(code.split('\n')):
        if 'return' in line and 'def' in code.split('\n')[index-1]:
            return True
    return False

def get_external_libs(code):
    return code.count('import')

def get_cyclomatic_complexity(code):
    analysis = lizard.analyze_file.analyze_source_code("0.py", code)
    try:
        return analysis.function_list[0].cyclomatic_complexity
    except:
        return -1

def export_checkpoints(df, llm, out):
    llm = llm.split('_')[0]

    with pd.ExcelWriter(f'{out}/{llm}.xlsx') as er:
        df.to_excel(er, index=False, sheet_name='Original')
        
        df = df[df['is_one_liner'] == False]
        df.to_excel(er, index=False, sheet_name='Step 1')
        
        df = df[df['external_libs'] == 0]
        df.to_excel(er, index=False, sheet_name='Step 2')

        df = df[df['cyclomatic_complexity'] > CYCLOMATIC_COMPLEXITY_THRESHOLD]
        df.to_excel(er, index=False, sheet_name='Step 3')


def filter(solutions, out):
    df = pd.read_excel('./details.xlsx')
    df['ID'] = df['ID'].astype(int)
    df['is_one_liner'] = False
    df['external_libs'] = 0
    df['cyclomatic_complexity'] = 0
    for zipfile in os.listdir(solutions):
        print(f'Extracting {zipfile}')
        with ZipFile(f'{solutions}/{zipfile}', 'r') as z:
            for file in z.namelist():
                if 'humaneval' in file and file.endswith('.py'):
                    code_challenge_number = file.split('/')[-2].split('_')[1]
                    
                    with z.open(file) as f:
                        code = f.read().decode('utf-8')
                        df.loc[df['ID'] == int(code_challenge_number), 'is_one_liner'] = check_oneliner(code)
                        df.loc[df['ID'] == int(code_challenge_number), 'external_libs'] = get_external_libs(code)
                        df.loc[df['ID'] == int(code_challenge_number), 'cyclomatic_complexity'] = get_cyclomatic_complexity(code)

        export_checkpoints(df, zipfile, out)


if __name__ == '__main__':
    solutions_folder = SOLUTIONS_FOLDER #sys.argv[1]
    output_folder = OUTPUT_FOLDER #sys.argv[2]
    filter(solutions_folder, output_folder)
