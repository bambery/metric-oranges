class Airport:
    # key is locid
    collection = {}

    def __init__(self, name, state, city, locid, hub, enplaned):
        self.name = name
        self.state = state
        self.city = city
        self.locid = locid
        self.hub = hub
        self.enplaned = enplaned

    def __repr__(self):
        return f'Airport(name: {self.name}, {self.city}, {self.state}, locid: {self.locid}, hub: {self.hub}), enplaned: {self.enplaned}'
