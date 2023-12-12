from typing import List
from common import * 

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

def log_info(s):
    print(f'[INFO] {s}')
