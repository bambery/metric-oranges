class Fips:
    # list of all FIPS by code
    collection = {}

    def __init__(self, county_name, state_abbr, state_code, county_code):
        self.code = ''.join([state_code, county_code])
        self.county = county_name
        self.state = state_abbr
        self.cbsa_code = None # populated by process_inputs/cbsa_fips_mapping.py
        self.node_id = None # populated by process_inputs/build_nodes.py
        self.airports = set() # conditionally populated by process_inputs/airports.py
        self.adjacent_fips_codes = set() # populated by process_inputs/fips_adjacency.py in next step
        # FIXME: do I need to keep this on FIPS?
        self.adjacent_node_ids = set() # populated by process_inputs/fips_adjacency.py in next step
        # only used for testing combined with change in classes/Node.py, process_inputs/deaths_by_node
#        self.deaths = {}
        Fips.collection[self.code] = self

    def __repr__(self):
        return f'FIPS({self.code}: Node: {self.node_id}; {self.county}, {self.state}; cbsa: {self.cbsa_code}; airports: {self.airports})'

    @classmethod
    def get_node_id(cls, fips_code):
        return cls.collection[fips_code].node_id

    @classmethod
    def get(cls, code):
        return cls.collection[code]
