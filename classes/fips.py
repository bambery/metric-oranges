class Fips:
    # list of all FIPS by code
    collection = {}

    def __init__(self, code, county, state, class_code, cbsa = None):
        self.code = code
        self.county = county 
        self.state = state
        self.cbsa = cbsa
        self.class_code = class_code # see doc for details - unused currently
        self.airports = set()

    def __repr__(self):
        return f'FIPS({self.code}: {self.county}, {self.state}, cbsa: {self.cbsa}, class code: {self.class_code}, airports: {self.airports})'
