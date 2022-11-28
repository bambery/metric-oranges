class Cbsa:

    # list of all CBSAs by code
    collection = {}

    def __init__(self, code, name, msa_designation, fips = None):
        self.code = code
        self.name = name
        self.msa_designation = msa_designation # metro/micro
        self.uid = None # populated by process_inputs/build_uids.py
        self.fips_codes = set()
        if fips:
            self.fips_codes.add(fips) # python wants to turn a string into a list of chars >:(, can't initialize with a string
        self.airports = set()

    def __repr__(self):
        return f'Cbsa("{self.code}", UID: {self.uid}, name: "{self.name}", msa designation: "{self.msa_designation}",\nfips: {self.fips_codes},\n{self.airports})'
