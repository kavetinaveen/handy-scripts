# Import required packages
import pandas as pd
import numpy as np
import itertools

# Read sample data and results file
df = pd.read_csv('./Toto_2.csv')
result = pd.read_csv('./result.csv')

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
    df['tmp'] = df.apply(lambda x: [str(x['1']), 'X' if x['X'] else '0', '2' if x['2'] else '0'], axis=1)
    df['tmp'] = df.apply(lambda x: [y for y in x['tmp'] if y != '0'], axis=1)
    if generate_all:
        pos_sol = [['1', 'X', '2']]*len(df)
    else:
        pos_sol = df['tmp'].tolist()
    result_list = [str(x) for x in result['realresult'].tolist()]
    sol = []
    k = 0
    for element in itertools.product(*pos_sol):
        sol.append(list(element))
        count = 0
        for i, j in zip(result_list, list(element)):
            if i == j:
                count += 1
        if count>11:
            print(f"{count} choices correct out of 15 at index {k}")
        if list(element) == result_list:
            print("Congratulations!!!")
        k += 1
    return sol

results_all = pd.DataFrame(generate_solutions(df))
results_all.to_csv('all_solutions.csv', index=False)
results_all
