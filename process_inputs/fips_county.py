import pandas as pd
# local imports
import shared.utils as utils
import shared.helpers as helpers
import classes.fips import Fips

inputs = utils.get_inputs_dir()

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', None)

file_path_place_cbsa = inputs.joinpath("census", "place_cbsa", "place05-cbsa06.xls")

# columns
# 0: state code, 1: state (2 letters), 2: place code, 3: place name, 4: county code, 5: county name, 6: cbsa code, 7: cbsa name, 8: cbsa lsad, 9: cbsa part indicator, 10: principal city indicator, and I don't care about the rest

def build fips_maps():
    def convert_place_cbsa_to_csv():
        places = pd.read_excel(
                file_path_place_cbsa,
                header = 0,
                usecols = [0, 1, 3, 4, 6, 10],
                )
        return places.to_csv(None, index=False, header=False)

    places = convert_place_cbsa_to_csv()

    place_cbsa = {}




