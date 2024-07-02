import os
import sys
import pandas as pd
import re
import zipfile

SOLUTIONS_FOLDER = './solutions'
OUTPUT_FOLDER = './out'


def filter(solutions, out):
    

if __name__ == '__main__':
    solutions_folder = SOLUTIONS_FOLDER #sys.argv[1]
    output_folder = OUTPUT_FOLDER #sys.argv[2]
    df = pd.read_excel('./details.xlsx')
    df.to_excel('./out/details_filtered.xlsx', index=False)
