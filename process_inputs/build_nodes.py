from classes.node import Node
from classes.fips import Fips
from classes.cbsa import Cbsa
from classes.airport import Airport

def process_fips_for_nodes():
    for [fips_code, fips] in Fips.collection.items():
        node = None
        cbsa = None
        if not fips.cbsa_code:
            if fips_code == "08097":
                breakpoint()
            node = Node("FIPS", fips.county + "_" + fips.state)
            node.airports = node.airports.union(fips.airports)
        else:
            cbsa = Cbsa.collection[fips.cbsa_code]
            node = Node.get_by_cbsa(cbsa.code)
            if not node:
                node = Node("CBSA", cbsa.name)
            node.airports = node.airports.union(cbsa.airports)
            # associate CBSA with UID
            cbsa.node_id = node.id_

        node.cbsa_code = fips.cbsa_code
        node.fips_codes.add(fips_code)
        # associate the FIPS with the UID
        fips.node_id = node.id_

        # associate airports with a uid
        airport = None
        for locid in node.airports:
            Airport.collection[locid].node_id = node.id_
