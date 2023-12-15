from typing import List
from common import * 
import pandas as pd

def print_option(option):
    for k in option.keys():
        print(f'{k}. {option[k].name}')

def validate_input(inputs: List[Input]):
    errors = []
    ret = {}

    for x in inputs:
        if x.type == 'any':
            ret[x.name] = input(f'{x.name}: ')
        elif x.type == 'int':
            try:
                ret[x.name] = int(input(f'{x.name}: '))
            except ValueError:
                errors.append(f'{x.name} should be int')

    return ret, errors

def log_info(s, nl=True):
    if nl:
        print()
    print(f'[INFO] {s}')

def print_headline(s):
    # Determine the width of the login box
    box_width = 50

    # Create the login interface
    headline = f"""
+{'=' * (box_width - 2)}+
|{s:^{box_width-2}}|
+{'=' * (box_width - 2)}+
    """
    print(headline)

def print_table_dataframe(data, title):
    df = pd.DataFrame(data)
    if len(df) < 1:
        log_info('no data avaiable', False)
        return

    print(title)
    print(df)
    print()
