# this file reads in the adjacency file and updates the FIPS so they contain their own adjacent FIPS

import csv

# local imports
import shared.utils as utils
import shared.helpers as helpers
from classes.fips import Fips
from classes.node import Node

inputs = utils.get_inputs_dir()
# note that this file is a windows encoded text file, ie windows-1252
# header: none
# [0] - county, state name
# [1] - fips
# [2] - name of adjacent county
# [3] - fips of adjacent county
file_path_fips_adjacency = inputs.joinpath("census", "county_adjacency_2010","county_adjacency.txt")

remapped_fips = { '02270': '02158', '46113': '46102', '51515': '51019' }

def build_edges():
    with open(file_path_fips_adjacency, encoding='cp1252', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row[1]: # if there is an entry in col 1, then this is begins a new adjacency entry. Cannot check col 0 as the file has a typographical error in that column
                if row[1] == "27165": # there is a typo in the input file that omits Watonwan County, MN's name
                    county = "Watonwan County"
                    state = "MN"
                else:
                    county, state = row[0].split(', ')
                if state not in helpers.ALL_US_STATES:
                    continue # skip non-US states
                curr_fips = remapped_fips.get(row[1], row[1])
            else: # there is no fips in col 0, then we are in the middle of assigning adjacencies
                county, state = row[2].split(', ')
                if state not in helpers.ALL_US_STATES:
                    continue # skip non-US states

            adj_fips = remapped_fips.get(row[3], row[3])

            if curr_fips == adj_fips:
                continue # when collecting fips adjacencies under CBSA, will get several self-references
            elif curr_fips == '02261' or adj_fips == '02261':
                continue # skip old Valdez-Cordova and fill manually
            elif curr_fips in ['02220', '02195'] and adj_fips in ['02220', '02195']:
                continue # do not add edge between Sitka and Petersburg


            curr_fips_obj = Fips.collection[curr_fips]
            adj_fips_node_id = Fips.get_node_id(adj_fips)

            # associate adjacent FIPSs and UIDs on the Fips object
            curr_fips_obj.adjacent_fips_codes.add(adj_fips)
            curr_fips_obj.adjacent_node_ids.add(adj_fips_node_id)

            # create an "adjacent county" edge
            Node.get(curr_fips_obj.node_id).adjacent_nodes.add(adj_fips_node_id)


    # finished processing file - now to manually add new edges
    def add_adj_edges(fips_code_a, fips_code_b):
        node_a = Node.get_by_fips(fips_code_a)
        node_b = Node.get_by_fips(fips_code_b)
        fips_a = Fips.get(fips_code_a)
        fips_b = Fips.get(fips_code_b)

        node_a.adjacent_nodes.add(node_b.id_)
        node_b.adjacent_nodes.add(node_a.id_)
        fips_a.adjacent_fips_codes.add(fips_code_b)
        fips_a.adjacent_node_ids.add(fips_b.node_id)
        fips_b.adjacent_fips_codes.add(fips_code_a)
        fips_b.adjacent_node_ids.add(fips_a.node_id)

    # add edges for new Chugach Census Area
    # 02063 Chugach
    #           02020 Anchorage
    #           02122 Kenai
    #           02066 Copper River
    #           02282 Yukatat
    #           02170 Manatuska-Susitna
    [ add_adj_edges('02063', fips) for fips in ['02020', '02122', '02066', '02282', '02170']]

    # add edges for new Copper River Census Area
    # 02066 Copper River
    #           02240 Southeast Fairbanks
    #           02170 Manatuska-Susitna
    #           02063 Chugach
    #           02282 Yukatat
    [ add_adj_edges('02066', fips) for fips in ['02240', '02170', '02063', '02282']]

    # add edges where FIPS borders changed
    # 02105 Hoonah-Angoon -         02198 Prince of Wales-Hyder
    add_adj_edges('02105', '02198')
    # 02198 Prince of Wales-Hyder - 02220 Sitka
    add_adj_edges('02198', '02220')
    # 02195 Petersburg -            02110 Juneau
    add_adj_edges('02195', '02110')
