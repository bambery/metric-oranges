class Uid:

    collection = {}

    def __init__(self. uid_code, category):
        self.uid = uid_code
        self.category = category # "F" = FIPS, "C" = CBSA
        self.adjacent = set() # geographically adjacent counties by UID
        self.airports = set() # airports located within this region

#    @classmethod
#    def lookup_by_fips(cls, fips):

#    def edges():
        # return an Edges.collection[uid] call, do not store twice
