import process_inputs.fips_counties as fc
import process_inputs.cbsa_fips_mapping as cbsa
import process_inputs.fips_place_cbsa as fpc
import process_inputs.airports as air
import process_inputs.build_nodes as bn
import process_inputs.jhu as jhu
import process_inputs.adjacency_edges as adje
import process_inputs.flight_edges as fled

import process_outputs.process_outputs as po

from classes.node import Node
from classes.fips import Fips
from classes.cbsa import Cbsa
from classes.airport import Airport

# 01 - fips_counties.py
# first: read in a complete list of all FIPS in the US - there are 3,235 in this file
fc.build_fips()

# 02 - cbsa_fips_mapping.py
# next map each fips to a CBSA, if it exists
cbsa.build_CBSA_maps()

# 3 - fips_place_cbsa
# used for associating an airport to a county
# returns a lookup for place_cbsa["place name"] -> [fips_code, cbsa_code]
place_cbsa = fpc.build_fips_maps()

# 4 - airports
# link airports to CBSAs and FIPS
airports = air.process_airports(place_cbsa)
del place_cbsa

# 5 - construct Nodes by CBSA for counties that have them, or by FIPS for those without
bn.process_fips_for_nodes()

# 6 - process JHU daily files into weekly reports
jhu.create_weekly_counts()

# 7 - process county adjacencies
adje.build_edges()

#8 - build flight routes
fled.process_flight_edges()

#9 write airport reports
po.generate_airport_report()

print("you are in main")
breakpoint()
