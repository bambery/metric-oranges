###
#
# this file proceses and fills a FIPS lookup with Fips.collection[fips_code] -> returns Fips object
# this file also produces a place -> cbsa lookup as a dict with place_cbsa[place_name] -> returns cbsa_code 
#
###
import pandas as pd
# local imports
import shared.utils as utils
import shared.helpers as helpers
from classes.fips import Fips

inputs = utils.get_inputs_dir()

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', None)

file_path_place_cbsa = inputs.joinpath("census", "place_cbsa", "place05-cbsa06.xls")

# columns
# 0: state code, 1: state (2 letters), 2: place code, 3: place name, 4: county code, 5: county name, 6: cbsa code, 7: cbsa name, 8: cbsa lsad, 9: cbsa part indicator, 10: principal city indicator, and I don't care about the rest

def build_fips_maps():
    def convert_place_cbsa_to_csv():
        places = pd.read_excel(
                file_path_place_cbsa,
                header = 0,
                usecols = [0, 1, 3, 4, 5, 6],
                dtype = {0: str, 1:str, 2: str, 3: str, 4:str, 5: str}
                )
        return places.to_csv(None, index=False, header=False)

    # the place names in the place-cbsa file are all appended with a word which I can find no list nor definition of. Places that have the word "City" as part of their name have the word "city" (in lower case) appended to the end anyway.
    # there are 2 "places" with commas, neither have airports
    # there are 5 cities in the US named "Lynchburg" in MS, OH, SC, TN, and VA, and one named "Lynch City" in Kentucky. I cannot. 
    def strip_ending(s):
        words = s.split(" ")
        if len(words) > 6: return ""

        last = words.pop()
        if last == "(part)":
            words.pop()
        return " ".join(words)

    places = convert_place_cbsa_to_csv()

    place_cbsa = {}

    for row in places.splitlines():
        try:
            fips_state, state_name, place_name, fips_county, county_name, cbsa_code = row.split(",") 
        except:
            print("u inside")
            breakpoint()
        full_fips = fips_state + fips_county 
        myfips = Fips(full_fips, county_name, state_name, cbsa_code) 

        Fips.collection[full_fips] = myfips
        place_cbsa[strip_ending(place_name)] = cbsa_code 
    return place_cbsa
