# this file reads in the adjacency file and updates the FIPS so they contain their own adjacent FIPS

import csv

# local imports
import shared.utils as utils
import shared.helpers as helpers
from classes.fips import Fips
from classes.edge import Edge
from classes.airport import Airport

inputs = utils.get_inputs_dir()
# note that this file is a windows encoded text file, ie windows-1252
# header: none
# [0] - county, state name
# [1] - fips
# [2] - name of adjacent county
# [3] - fips of adjacent county
file_path_fips_adjacency = inputs.joinpath("census", "county_adjacency_2010","county_adjacency.txt")

def build_edges():
    with open(file_path_fips_adjacency, encoding='cp1252', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row[1]: # if there is an entry in col 0, then this is begins a new adjacency entry
                if row[1] == "27165": # there is a typo in the input file that omits Watonwan County, MN's name
                    county = "Watonwan County"
                    state = "MN"
                else:
                    county, state = row[0].split(', ')
                if state not in helpers.ALL_US_STATES:
                    continue # skip non-US states
                curr_fips = row[1]
            else: # there is no fips in col 0, then we are in the middle of assigning adjacencies
                county, state = row[2].split(', ')
                if state not in helpers.ALL_US_STATES:
                    continue # skip non-US states

            my_fips = Fips.collection[curr_fips]
            other_fips = Fips.collection[row[3]]
            if my_fips == other_fips: continue # when collecting fips adjacencies under CBSA, will get several self-references

            # associate adjacent FIPSs and UIDs on the Fips object
            my_fips.adjacent_fips.add(other_fips.code)
            my_fips.adjacent_uids.add(other_fips.uid)

            # create an "adjacent county" edge
            adj_edge = Edge(my_fips.uid, other_fips.uid, "AC")
            if my_fips.uid not in Edge.collection:
                Edge.collection[my_fips.uid] = set()
            Edge.collection[my_fips.uid].add(adj_edge)
