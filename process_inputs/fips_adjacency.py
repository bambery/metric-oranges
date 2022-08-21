import csv

# local imports
import shared.utils as utils

inputs = utils.get_inputs_dir() 
# note that this file is a windows encoded text file, ie windows-1252
# header: none
# [0] - county, state name
# [1] - fips
# [2] - name of adjacent county
# [3] - fips of adjacent county
file_path_fips_adjacency = inputs.joinpath("census", "county_adjacency.txt")

def build_fips_adjacency():
    edges = {}
    with open(file_path_fips_adjacency, encoding='cp1252', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row[1]=="72001": # if we hit Puerto Rico, we are done
                break
            elif row[1]: # if there is an entry in col 1, then this is begins a new edges entry 
                curr = int(row[1])
                edges[curr] = []
            else: # there is no fips in col 1 and we are in the middle of assigning edges
                edges[curr].append(int(row[3]))
    return edges 


print("you imported a file")
