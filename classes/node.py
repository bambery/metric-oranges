import itertools
from classes.fips import Fips
from classes.cbsa import Cbsa

# this class is a "universal identifier" for the regions considered in this project. Each one represents a CBSA if applicable, and if not, the FIPS inbetween

# there are 1302 Nodes representing FIPS that do not belong to a CBSA, and 927 Nodes representing CBSAs

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

        # who decided "id" was a great name for a built-in method?
        self.id_ = str(Node.__get_next_id())
        self.adjacent_nodes = set() # geographically adjacent Nodes
        self.airports = set() # airports located within this region
        self.fips_codes  = set() # any fips contained
        self.cbsa_code = None # if this Node represents a CBSA, this field will be populated
        # key is date of week start YY-MM-DD, val is death count
        self.deaths = {}
        # add to collection
        Node.collection[self.id_] = self

    def __repr__(self):
        return f'Node( id: {self.id_}, category: {self.category} \nCBSA: {self.cbsa_code}; FIPS codes: {self.fips_codes}),\n airports: {self.airports}, \nadjacent nodes: {self.adjacent_nodes}'

    @classmethod
    def add_deaths(cls, id_, week_name, deaths):
        cls.collection[id_].deaths[week_name] = cls.collection[id_].deaths.get(week_name, 0) + int(deaths)
        # if you want to see deaths on FIPS, uncomment adding deaths to FIPS class
        #Fips.collection[id_].deaths[week_name] = cls.collection[id_].deaths.get(week_name, 0) + int(deaths)

    @classmethod
    def get(cls, id_):
        return cls.collection[id_]

    @classmethod
    def get_by_fips(cls, fips_code):
        id_ = Fips.get_node_id(fips_code)
        return cls.collection[id_]

    @classmethod
    def get_by_cbsa(cls, cbsa_code):
        id_ = Cbsa.get_node_id(cbsa_code)
        return cls.collection.get(id_)
