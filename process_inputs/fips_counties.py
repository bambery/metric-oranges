import csv
# local imports
import shared.utils as utils
import shared.helpers as helpers
from classes.fips import Fips

inputs = utils.get_inputs_dir()

file_path_county_fips = inputs.joinpath("census", "county_fips", "national_county.txt")

# columns
# 0: 2 char state code, 1: fips state code, 2: fips county code, 3: county name, 4: class_code

def build_fips():
    with open( file_path_county_fips, newline='' ) as fips_file:
        reader = csv.reader(fips_file)
        for row in reader:
            state, fips_state, fips_county, county_name, class_code = row
            
            if state not in helpers.ALL_US_STATES: continue; # skip AS, GU, MP, VI, PR, UM 
            full_fips = fips_state + fips_county
            myfips = Fips(full_fips, county_name, state, class_code) 
            Fips.collection[full_fips] = myfips
