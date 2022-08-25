import process_inputs.fips_counties as fc
import process_inputs.cbsa_fips_mapping as cbsa
import process_inputs.fips_place_cbsa as fpc 
import process_inputs.airports as air
import process_inputs.build_uids as bu
import process_inputs.fips_adjacency as fa

# 01 - fips_counties.py
# first: read in a complete list of all FIPS in the US - there are 3,235 in this file
fc.build_fips()

# 02 - cbsa_fips_mapping.py
#complete
cbsa.build_CBSA_maps()

# 3 - fips_place_cbsa
# complete
# returns a lookup for place_cbsa["place name"] -> [fips_code, cbsa_code]
place_cbsa = fpc.build_fips_maps()

# 4 - airports
# complete
airports = air.process_airports(place_cbsa)
del place_cbsa # need to check if there are other references out there - this file is only used to process airports

# 5 - process FIPS adjacency file and update ajacent counties for each Fips instance 
# complete
fa.build_fips_adjacency()

# 6 - construct UIDs
# in progress
bu.process_fips_for_uid()

print("you are in main")
breakpoint()
