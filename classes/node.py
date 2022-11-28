import itertools
from classes.fips import Fips

# this class is a "universal identifier" for the regions considered in this project. Each one represents a CBSA if applicable, and if not, the FIPS inbetween

class Node:

    collection = {}
    __id_counter = itertools.count(1)

    @classmethod
    def __get_next_id(cls):
        return next(cls.__id_counter)

    def __init__(self, category):
        category = category.upper()
        if category in ["FIPS", "F"]:
            self.category = "F"
        elif category in ["CBSA", "C"]:
            self.category = "C"
        else:
            raise ValueError("Must pass 'fips' or 'cbsa' when creating a new Node")

        self.id = Node.__get_next_id()
        self.adjacent = set() # geographically adjacent Nodes
        self.airports = set() # airports located within this region
        self.fips_codes  = set() # any fips contained
        self.cbsa_code = None # if this Node represents a CBSA, this field will be populated
        # key is date of week start YY-MM-DD, val is death count
        self.deaths = {}
        # add to collection
        Node.collection[self.id] = self

    def __repr__(self):
        return f'Node( id: {self.id}, category: {self.category} \nCBSA: {self.cbsa_code}; FIPS codes: {self.fips_codes}),\n airports: {self.airports}'

    @classmethod
    def add_deaths(cls, id, week_name, deaths):
        cls.collection[id].deaths[week_name] = cls.collection[id].deaths.get(week_name, 0) + int(deaths)

    @classmethod
    def get(cls, id):
        return cls.collection[id]

    @classmethod
    def get_by_fips(fips):
        uid = Fips.get_uid(fips)
        return cls.collection[uid]
