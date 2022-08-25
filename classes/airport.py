import shared.helpers as helpers

# there are 368 NPIAS hub-ranked airports from 2017-2021. I omit one, "Block Island" in RI, for a total of 367.

class Airport:
    # key is locid
    collection = {}

    def __init__(self, name, state, city, locid, hub, enplaned, cbsa, fips):
        self.name = name
        self.state = state
        self.city = city
        self.locid = locid
        self.hub = hub
        self.enplaned = enplaned
        self.cbsa_code = cbsa
        self.fips_code = fips
        self.uid = None # assigned in process_inputs/build_uids.py

    def __repr__(self):
        return f'Airport({self.locid}; name: {self.name}; location: {self.city}, {self.state}; hub: {self.hub}; enplaned: {self.enplaned}; cbsa: {self.cbsa_code}, fips: {self.fips_code}\n'

    @classmethod
    def by_state(cls, state):
        return { val for val in cls.collection.values() if val.state == state }

    @classmethod
    def all_state_count(cls):
        count = {}
        for state in helpers.ALL_US_STATES:
            count[state] = len(cls.by_state(state))
        return count
