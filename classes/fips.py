class Fips:
    # list of all FIPS by code
    collection = {}

    def __init__(self, county_name, state_abbr, state_code, county_code):
        self.code = ''.join([state_code, county_code])
        self.county = county_name
        self.state = state_abbr
        self.cbsa_code = None # populated by process_inputs/cbsa_fips_mapping.py
        self.uid = None # populated by process_inputs/build_uids.py
        self.airports = set() # conditionally populated by process_inputs/airports.py
        self.adjacent_fips = set() # populated by process_inputs/fips_adjacency.py in next step
        self.adjacent_uids = set() # populated by process_inputs/fips_adjacency.py in next step
        Fips.collection[self.code] = self

    def __repr__(self):
        return f'FIPS({self.code}: UID: {self.uid}; {self.county}, {self.state}; cbsa: {self.cbsa_code}; airports: {self.airports})'

    @classmethod
    def get_uid_code(cls, fips_code):
        return cls.collection[fips_code].uid
