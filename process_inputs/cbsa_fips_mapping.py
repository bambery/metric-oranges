import csv
import pandas as pd
# local imports
import shared.utils as utils
import shared.helpers as helpers

inputs = utils.get_inputs_dir()

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', None)


file_path_cbsa_list1 = inputs.joinpath("census", "list1_2020.xls")
file_path_cbsa_csv = inputs.joinpath("census", "list1_2020.csv")
# the first 10 chars indicate this is an MS-OLE2 encoded file from Excel 97. This format is extraordinarily difficult for python to parse.
# $ print(repr(open(file_path_cbsa_list1, 'rb').read(10)))
#b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1\x00\x00'
# I need to parse this file line by line to build several lookup dicts, which I appear to be unable to do.
# Therefore, I need to parse this file with Pandas (and discard the first two lines), write it to csv, then read that in again. I spent many hours attempting to find another way: can't seem to without writing an XLS parser.

# the columns of interest:
# columns
# 0: CBSA code, 1: metro division code, 2: csa code, 3: cbsa title, 4: metro/micro designation, 5: metro division title, 6: csa title, 7. county/county equivalent, 8. state name, 9. FIPS state code, 10: FIPS county code, 11: central or outlying

def convert_to_csv():
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


    cbsas = pd.read_excel(
            file_path_cbsa_list1, 
            skiprows = 2, 
            skipfooter = 4,
            header = 0, 
            usecols = [0, 3, 4, 7, 8, 9, 10, 11], 
            names = ["CBSA Code", "CBSA Name", "Metro/Micro", "County", "State", "FIPS State Code", "FIPS County Code", "Central/Outlying"],
            dtype = {'CBSA Code': str, 'FIPS State Code': str, 'FIPS County Code': str},
            converters={ "Metro/Micro": micro_metro, "State": state_abbreviation },
            )

    cbsas.to_csv(file_path_cbsa_csv, index = False)

