import itertools
from classes.fips import Fips

# this class is a "universal identifier" for the regions considered in this project. Each one represents a CBSA if applicable, and if not, the FIPS inbetween

class Uid:

    collection = {}
    __uid_counter = itertools.count()

    @classmethod
    def __get_next_uid(cls):
        return next(cls.__uid_counter)

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
        # key is date of week start YY-MM-DD, val is death count
        self.deaths = {}
        # add to collection
        Uid.collection[self.code] = self

    def __repr__(self):
        return f'UID( my_uid: {self.code}, category: {self.category} \nCBSA codes: {self.cbsa_codes}; FIPS codes: {self.fips_codes}),\n airports: {self.airports}'

    @classmethod
    def add_deaths(cls, uid, week_name, deaths):
        cls.collection[uid].deaths[week_name] = cls.collection[uid].deaths.get(week_name, 0) + int(deaths)

    @classmethod
    def get(cls, uid):
        return cls.collection[uid]

    @classmethod
    def get_by_fips(fips):
        uid = Fips.get_uid(fips)
        return cls.collection[uid]
