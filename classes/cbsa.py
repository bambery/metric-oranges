# note: there are 939 CBSAs listed in list1_v2020, 927 in US States
#
# regarding distribution of how many FIPS are in each CBSA, there are 598 CBSAs with only one FIPS assigned, 155 with 2, and so on as follows:
#    {1: 598, 2: 155, 3: 66, 4: 44, 5: 18, 6: 11, 7: 10, 8: 5, 10: 4, 11: 4, 14: 2, 15: 2, 29: 1, 16: 1, 9: 1, 13: 1, 23: 1, 17: 1, 19: 1, 25: 1})
# Therefore, only 329 CBSAs represent an area containing more than one FIPS.

class Cbsa:

    # list of all CBSAs by code
    collection = {}

    def __init__(self, code, name, msa_designation, fips = None):
        self.code = code
        self.name = name
        self.msa_designation = msa_designation # metro/micro
        self.node_id = None # populated by process_inputs/build_node_ids.py
        self.fips_codes = set()
        if fips:
            self.fips_codes.add(fips) # python wants to turn a string into a list of chars >:(, can't initialize with a string
        self.airports = set()

    def __repr__(self):
        return f'Cbsa || Cbsa code:{self.code}, Node id: {self.node_id}, name: {self.name}, msa designation: {self.msa_designation},\nfips_codes: {self.fips_codes},\nairports: {self.airports})'
    @classmethod
    def get_node_id(cls, cbsa_code):
        return cls.collection[cbsa_code].node_id

    @classmethod
    def get(cls, code):
        return cls.collection[code]
