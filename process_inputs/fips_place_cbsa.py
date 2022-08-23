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
    # there are 5 cities in the US named "Lynchburg" in MS, OH, SC, TN, and VA, and one named "Lynch City" in Kentucky. I cannot. 

    # should be refactored. Check if last item is all lowercase or CDP. if yes, pop, repeat
    def normalize_name(place):

        if place == "Lexington-Fayette": 
            return "LEXINGTON" # airport is named after truncated county name
        elif place == "Hartsville-Trousdale": # airport named after county 
            return place.upper()
        elif place == "Louisville-Jefferson County (balance)": # airport is named after truncated county name
            return "LOUISVILLE"
        elif place == "Butte-Silver Bow (balance)":
            return "BUTTE"
        elif place == "Nashville-Davidson (balance)":
            return "NASHVILLE"

        words = place.split(" ")
        last = words.pop()
        if last == "(part)":
            words.pop()
        elif last == "(balance)":
            second_to_last = len(words)-1
            if words[second_to_last].islower() or words[second_to_last] == "CDP": 
                words.pop()
        elif len(words) > 1:
            second_to_last = len(words)-1
            if words[second_to_last] == "and":
                words.pop()
                words.pop()

        try:
            words = list(map(lambda word: word.upper(), words))
            loc = words.index("ST.") if "ST." in words else -1
        except:
            print("theres no words??")
            breakpoint()
        if loc > -1:
            words[loc] = "ST"

        return " ".join(words)
    
    def state_places(state):
        return {key for key in place_cbsa.keys() if key.startswith(state)}


    places = convert_place_cbsa_to_csv()

    place_cbsa = {}

    for row in places.splitlines():
        place_info = row.split(",") # two "places" have commas in their name, neither have airports
        if len(place_info) > 6:
            continue
        fips_state, state_name, place_name, fips_county, county_name, cbsa_code = place_info 

        full_fips = fips_state + fips_county 

        if place_name == "St. Cloud city (part)" and fips_county in ['009', '145']:
            continue # 3 different places in MN named this, with different FIPS and CBSAs. I am choosing the one with the airport I want
        place_name = normalize_name(place_name)

        myfips = Fips(full_fips, county_name, state_name, cbsa_code) 

        Fips.collection[full_fips] = myfips

        state_place = state_name + "_" + place_name
        if state_place in place_cbsa:
            continue # choose the first instance of ("part") and skip the rest.
        place_cbsa[state_place] = { "cbsa": cbsa_code, "fips": full_fips }
    return place_cbsa
