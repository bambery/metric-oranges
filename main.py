#import process_inputs.fips_adjacency as fa
#import process_inputs.cbsa_fips_mapping as cbsa
#import process_inputs.fips_county as fc
import process_inputs.airports as air

airports = air.process_airports()

# complete
#place_cbsa = fc.build_fips_maps()


#complete
#fips_cbsa, cbsa_map = cbsa.build_CBSA_maps()

# working - not ready to consume yet
#adjacent = fa.build_fips_adjacency()

print("you are in main")
breakpoint()
