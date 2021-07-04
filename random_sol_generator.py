# Import required packages
import pandas as pd
import numpy as np
import itertools

# Read sample data and results file
df = pd.read_excel('./toto.xlsx')
result = pd.read_excel('./result.xlsx')

# Function to generate solutions
def generate_solutions(df, generate_all=False):
    '''
    Description: function to generate possible solution for a given sample or all possible solutions
    :param df: sample 
    :param type: pandas dataframe
    :param generate_all: Whether to use the sample to generate solutions or generate all possible combinations
    :param type: boolean
    :return sol: list of all possible solutions or sample solutions generated for the given sample
    :return type: list of lists
    '''
    df['tmp'] = df.apply(lambda x: [x[1], 'X' if x['X'] else 0, 2 if x[2] else 0], axis=1)
    df['tmp'] = df.apply(lambda x: [y for y in x['tmp'] if y != 0], axis=1)
    if generate_all:
        pos_sol = [[1, 'X', x]]*len(df)
    else:
        pos_sol = df['tmp'].tolist()
    result_list = result['realresult'].tolist()
    sol = []
    for element in itertools.product(*pos_sol):
        sol.append(list(element))        
        if list(element) == result_list:
            print("Congratulations!!!")
    return sol
