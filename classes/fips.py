class Fips:
    # list of all FIPS by code
    collection = {}

    # hit this with a FIPS code to get the CBSA code if it exists, or return the FIPS if it doesn't. Used for accessing the oranges table.
    @classmethod
    def get_code(fips_code):
        if fips_code in collection:
            return collection[fips_code].cbsa
        else: 
            return fips_code

    def __init__(self, code, county, state, cbsa = None):
        self.code = code
        self.county = county 
        self.state = state
        self.cbsa = cbsa
        self.airports = set()

    def __repr__(self):
        return f'FIPS({self.code}: {self.county}, {self.state}, cbsa: {self.cbsa})'
