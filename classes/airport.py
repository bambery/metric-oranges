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
        self.destinations = set()
        self.node_id = None # assigned in process_inputs/build_nodes.py

    def __repr__(self):
        return f'Airport({self.locid}; name: {self.name}; location: {self.city}, {self.state}; hub: {self.hub}; enplaned: {self.enplaned}; cbsa: {self.cbsa_code}, fips: {self.fips_code}, node id: {self.node_id}\n'

    @classmethod
    def by_state(cls, state):
        return { val for val in cls.collection.values() if val.state == state }

    @classmethod
    def all_state_count(cls):
        count = {}
        for state in helpers.ALL_US_STATES:
            count[state] = len(cls.by_state(state))
        return count

    @classmethod
    def get_node_id(cls, locid):
        return Airport.collection[locid].node_id

    @classmethod
    def get(cls, locid):
        if locid in cls.collection.keys():
            return cls.collection[locid]
        else:
            return None

    # flight paths are not considered to be directional
    # we also only want flights for airports we are tracking
    @classmethod
    def add_flight_route(cls, origin_locid, dest_locid):
        origin_airport = cls.collection.get(origin_locid, None)
        if origin_airport:
            dest_airport = cls.collection.get(dest_locid, None)
            if dest_airport:
                origin_airport.destinations.add(dest_locid)
                dest_airport.destinations.add(origin_locid)
