import pandas as pd
# local imports
import shared.utils as utils
import shared.helpers as helpers
from classes.cbsa import Cbsa
from classes.fips import Fips

inputs = utils.get_inputs_dir()

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', None)

file_path_cbsa_list1 = inputs.joinpath("census", "list1", "list1_2020.xls")
# the first 10 chars indicate list1 is an MS-OLE2 encoded file from Excel 97. This format is difficult for Python to parse.
# $ print(repr(open(file_path_cbsa_list1, 'rb').read(10)))
#b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1\x00\x00'
# I need to parse this file line by line to build several lookup dicts, which I appear to be unable to do.
# Therefore, I need to parse this file with Pandas (and discard the first two lines), write it to csv (as a string in memory), then finally process the file. I spent many hours attempting to find another way: can't seem to without writing my own XLS parser.
# NOTE: The 2020 file is in the exact same format and will read in without changes

# columns
# 0: CBSA code, 1: metro division code, 2: csa code, 3: cbsa title, 4: metro/micro designation, 5: metro division title, 6: csa title, 7. county/county equivalent, 8. state name, 9. FIPS state code, 10: FIPS county code, 11: central or outlying

def build_CBSA_maps():
    def convert_list1_to_csv():
        def micro_metro(designation):
            if designation.startswith("Micro"):
                return "Micro"
            else:
                return "Metro"
        def state_abbreviation(abbr):
            abbr = abbr.upper()
            if abbr in helpers.US_STATES:
                return helpers.US_STATES[abbr]
            return None
        def replace_cbsa_comma(cbsa_name):
            return cbsa_name.replace(", ", "_")


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

        # optionally, write to temp file and read back in line by line
        return cbsas.to_csv(None, index = False, header = False)

    mycsv = convert_list1_to_csv()
    # my new csv string's columns
    # 0: CBSA Code, 1: CBSA Name, 2: Metro/Micro, 3: County Name, 4: State (2 letter code), 5: FIPS State Code, 6: FIPS County Code, 7: Central/Outlying

    # I need to build several lookups:
    # FIPS -> CBSA Code
    # County Name -> CBSA code ---- the way the county names are entered is chaotic, and I can better easily scrape them from another file. It is too much work to clean the names as they appear on this list
    # CBSA Code -> CBSA object  -- this is being done under Cbsa.collection

    for row in mycsv.splitlines():
        code, name, msa, county_name, state, fips_state, fips_county, location = row.split(",")
        if fips_state in helpers.ALL_US_FIPS:
            full_fips = fips_state + fips_county
            Fips.collection[full_fips].cbsa_code = code # map fips -> cbsa code
            if (code in Cbsa.collection):
                # have seen this CBSA before, update the list of FIPS assigned
                Cbsa.collection[code].fips_codes.add(full_fips)
            else:
                # create new CBSA entry
                mycbsa = Cbsa(code, name, msa, full_fips)
                Cbsa.collection[code] = mycbsa
