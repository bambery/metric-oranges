#import process_inputs.fips_adjacency as fa
#import process_inputs.cbsa_fips_mapping as cbsa
#import process_inputs.fips_place_cbsa as fpc 
#import process_inputs.airports as air
import process_inputs.fips_counties as fc

# 01 - fips_counties
# first: read in a complete list of all FIPS in the US - there are 3,235 in this file
fc.build_fips()

# 02 - cbsa_fips_mapping
#complete
#fips_cbsa, cbsa_map = cbsa.build_CBSA_maps()

# 3 - fips_place_cbsa
# complete
#place_cbsa = fpc.build_fips_maps()

# 4 - airports
# complete
#airports = air.process_airports(place_cbsa)


# 5 - fips_adjacency
# complete
#adjacent = fa.build_fips_adjacency()

# 6 - uid_adjacency
# not started

print("you are in main")
breakpoint()
