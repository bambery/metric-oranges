class Edge:
    # key is uid, returned is list of edges to this node
    collection = {}

    def __init__(self, my_uid, other_uid, category, weight = None):
        self.my_uid = my_uid
        self.other_uid = other_uid
        self.category = category # either "AC" for "adjacent county" or "FR" for "flight route" - the lone letters "A" and "F" are ambiguous in context
        self.weight = weight

    def __repr__(self):
        return f'Edge( my_uid: {self.my_uid}, other_uid: {self.other_uid}, category: {self.category}, weight: {self.weight} )\n'
