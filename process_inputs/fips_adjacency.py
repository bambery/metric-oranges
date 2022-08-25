# this file reads in the adjacency file and updates the FIPS so they contain their own adjacent FIPS

import csv

# local imports
import shared.utils as utils
import shared.helpers as helpers
from classes.fips import Fips

inputs = utils.get_inputs_dir() 
# note that this file is a windows encoded text file, ie windows-1252
# header: none
# [0] - county, state name
# [1] - fips
# [2] - name of adjacent county
# [3] - fips of adjacent county
file_path_fips_adjacency = inputs.joinpath("census", "county_adjacency_2010","county_adjacency.txt")

def build_fips_adjacency():
    adjacent = {}
    with open(file_path_fips_adjacency, encoding='cp1252', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row[0]: # if there is an entry in col 0, then this is begins a new adjacency entry 
                county, state = row[0].split(',')
                if state not in helpers.ALL_US_STATES:
                    continue # skip non-US states
                curr = int(row[1])
            else: # there is no fips in col 0, then we are in the middle of assigning adjacencies 
                county, state = row[2].split(',')
                if state not in helpers.ALL_US_STATES:
                    continue # skip non-US states
                Fips.collection[curr].adjacent.append(row[3])
