from classes.node import Node
from classes.fips import Fips
from classes.cbsa import Cbsa
from classes.airport import Airport

def process_fips_for_nodes():
    for [fips_code, fips] in Fips.collection.items():
        if fips.cbsa_code == None:
            node = Node("FIPS")
            node.airports = node.airports.union(fips.airports)
        else:
            cbsa = Cbsa.collection[fips.cbsa_code]
            node = Node.get_by_cbsa(cbsa.code)
            if not node:
                node = Node("CBSA")
            node.airports = node.airports.union(cbsa.airports)
            # associate CBSA with UID
            cbsa.node_id = node.id_

        node.cbsa_code = fips.cbsa_code
        node.fips_codes.add(fips_code)
        # associate the FIPS with the UID
        fips.node_id = node.id_

        # associate airports with a uid
        for airport in node.airports:
            Airport.collection[airport].node_id_ = node.id_
