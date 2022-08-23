class Cbsa:

    # list of all CBSAs by code
    collection = {}

    def __init__(self, code, name, msa_designation, fips = None):
        self.code = code
        self.name = name
        self.msa_designation = msa_designation
        self.fips = set()
        if fips:
            self.fips.add(fips) # python wants to turn a string into a list of chars >:(, can't initialize with a string
        self.airports = set()
        
    def __repr__(self):
        return f'Cbsa("{self.code}", "{self.name}", "{self.msa_designation}", fips: {self.fips})'
