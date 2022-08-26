class Fips:
    # list of all FIPS by code
    collection = {}

    def __init__(self, code, county, state, class_code, cbsa = None):
        self.code = code
        self.county = county 
        self.state = state
        self.cbsa_code = cbsa
        self.class_code = class_code # see doc for details - unused currently
        self.uid = None # populated by process_inputs/build_uids.py
        self.airports = set() # conditionally populated by process_inputs/airports.py
        self.adjacent_fips = set() # populated by process_inputs/fips_adjacency.py in next step
        self.adjacent_uids = set() # populated by process_inputs/fips_adjacency.py in next step

    def __repr__(self):
        return f'FIPS({self.code}: {self.county}, {self.state}, cbsa: {self.cbsa_code}, class code: {self.class_code}, airports: {self.airports})'

    @classmethod
    def get_uid(fips_code):
        return Fips.collection[fips_code].uid
