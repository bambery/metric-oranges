class Fips:
    # list of all FIPS by code
    collection = {}

    # hit this with a FIPS code to get the CBSA code if it exists, or return the FIPS if it doesn't. Used for accessing the oranges table.
    @classmethod
    def get_code(fips_code):
        if fips_code in collection:
            return collection[fips_code]
        else: 
            return fips_code

    def __init__(self, code, name, state, cbsa = None, cbsa_central = None):
        self.code = code
        self.name = name
        self.state = state
        self.cbsa = cbsa
        self.cbsa_central = cbsa_central

    def __repr__(self):
        return f'FIPS({self.code}: {self.name}, {self.state}, cbsa: {self.cbsa}, cbsa central: {self.cbsa_central})'
