from classes.fips import Fips

# this class is a "universal identifier" for the regions considered in this project. Each one represents a CBSA if applicable, and if not, the FIPS inbetween

class Uid:

    collection = {}
    __uid_counter = -1 

    @classmethod
    def __get_next_uid(cls):
        cls.__uid_counter +=1
        return cls.__uid_counter

    def __init__(self, category):
        category = category.upper()
        if category in ["FIPS", "F"]:
            self.category = "F"
        elif category in ["CBSA", "C"]:
            self.category = "C"
        else:
            raise ValueError("Must pass 'fips' or 'cbsa' when creating a new UID")

        self.code = Uid.__get_next_uid() 
        self.adjacent = set() # geographically adjacent counties by UID
        self.airports = set() # airports located within this region
        self.fips_codes  = set() # any fips contained
        self.cbsa_codes = set() # any cbsa contained

    def __repr__(self):
        return f'UID( my_uid: {self.code}, category: {self.category} \nCBSA codes: {self.cbsa_codes}; FIPS codes: {self.fips_codes}),\n airports: {self.airports}'
