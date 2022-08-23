#import process_inputs.fips_adjacency as fa
import process_inputs.cbsa_fips_mapping as cbsa
import process_inputs.fips_place_cbsa as fpc 
import process_inputs.airports as air

#complete
fips_cbsa, cbsa_map = cbsa.build_CBSA_maps()

# complete
place_cbsa = fpc.build_fips_maps()

airports = air.process_airports(place_cbsa)



# working - not ready to consume yet
#adjacent = fa.build_fips_adjacency()

print("you are in main")
breakpoint()
