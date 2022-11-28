import openpyxl
# local imports
import shared.utils as utils
import shared.helpers as helpers
from classes.fips import Fips

inputs = utils.get_inputs_dir()

file_path_county_fips = inputs.joinpath("census", "county_fips", "all-geocodes-v2020.xlsx")
#file_path_county_fips = inputs.joinpath("census", "county_fips", "national_county.txt")

#file_path_fips_lookup = inputs.joinpath("jhu", "UID_ISO_FIPS_LookUp_Table.csv")

# columns
# 0: 2 char state code, 1: fips state code, 2: fips county code, 3: county name, 4: class_code

def build_fips():
    wb = openpyxl.load_workbook(file_path_county_fips)
    ws = wb['all-geocodes-v2019']
    for row in ws.iter_rows(min_row=6, values_only=True):

        fips_state = row[1]
        fips_county = row[2]
        county_name = row[6]
        state_abbr = helpers.FIPS_US_STATE.get(fips_state, False)

        if state_abbr not in helpers.ALL_US_STATES or fips_county == '000': continue # skip AS, GU, MP, VI, PR, UM
        myfips = Fips(county_name, state_abbr, fips_state, fips_county)
