import csv
import pandas as pd
# local imports
import shared.utils as utils
import shared.helpers as helpers
from classes.cbsa import Cbsa

inputs = utils.get_inputs_dir()

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', None)


file_path_cbsa_list1 = inputs.joinpath("census", "list1_2020.xls")
# the first 10 chars indicate this is an MS-OLE2 encoded file from Excel 97. This format is extraordinarily difficult for python to parse.
# $ print(repr(open(file_path_cbsa_list1, 'rb').read(10)))
#b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1\x00\x00'
# I need to parse this file line by line to build several lookup dicts, which I appear to be unable to do.
# Therefore, I need to parse this file with Pandas (and discard the first two lines), write it to csv (as a string), then finally process the file. I spent many hours attempting to find another way: can't seem to without writing my own XLS parser.

# columns
# 0: CBSA code, 1: metro division code, 2: csa code, 3: cbsa title, 4: metro/micro designation, 5: metro division title, 6: csa title, 7. county/county equivalent, 8. state name, 9. FIPS state code, 10: FIPS county code, 11: central or outlying

def build_CBSA_maps(): 
    def micro_metro(s):
        if s.startswith("Micro"):
            return "Micro"
        else:
            return "Metro"
    def state_abbreviation(s):
        s = s.upper()
        if s in helpers.US_STATES:
            return helpers.US_STATES[s]
        return None 
    def replace_cbsa_comma(s):
        return s.replace(", ", "_")


    cbsas = pd.read_excel(
            file_path_cbsa_list1, 
            skiprows = 2, 
            skipfooter = 4,
            header = 0, 
            usecols = [0, 3, 4, 7, 8, 9, 10, 11], 
            names = ["CBSA Code", "CBSA Name", "Metro/Micro", "County", "State", "FIPS State Code", "FIPS County Code", "Central/Outlying"],
            dtype = {'CBSA Code': str, 'FIPS State Code': str, 'FIPS County Code': str},
            converters={ "Metro/Micro": micro_metro, "State": state_abbreviation, "CBSA Name": replace_cbsa_comma },
            )

    mycsv = cbsas.to_csv(None, index = False, header = False)

    # my new csv string's columns
    # 0: CBSA Code, 1: CBSA Name, 2: Metro/Micro, 3: County Name, 4: State (2 letter code), 5: FIPS State Code, 6: FIPS County Code, 7: Central/Outlying

    # I need to build several lookups:
    # FIPS -> CBSA Code  [if I wanted to use central/outlying here is where I would make FIPS an object]
    # County Name -> CBSA code
    # CBSA Code -> CBSA object 

    fips_cbsa = {}
    county_to_cbsa = {}

    for row in mycsv.splitlines():
        code, name, msa, county_name, state, fips_state, fips_county, location = row.split(",")
        if fips_state in helpers.ALL_US_FIPS:
            full_fips = fips_state + fips_county 
            fips_cbsa[full_fips] = code # map fips -> cbsa code 
            if (code in Cbsa.collection):
                # have seen this CBSA before, update the list of FIPS assigned
                Cbsa.collection[code].fips.add(full_fips) 
            else:
                # create new CBSA entry
                mycbsa = Cbsa(code, name, msa, full_fips)
                Cbsa.collection[code] = mycbsa
        else:
            print("the fps state code ", fips_state, " is not part of the 50 US states")

    breakpoint()
