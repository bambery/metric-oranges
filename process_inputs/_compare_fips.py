#####################################
# this file was used to generate differences between 2010 and 2020 fips codes and remains as a demonastration of the process. This file is not actively used.
#####################################
import openpyxl
import csv
# local imports
import shared.utils as utils
import shared.helpers as helpers
from classes.fips import Fips

inputs = utils.get_inputs_dir()

fips_file_2010 = inputs.joinpath("census", "county_fips", "national_county.txt")

fips_file_2020 = inputs.joinpath("census", "county_fips", "all-geocodes-v2020.xlsx")

fips_2010 = {}
fips_2020 = {}

def build_2010_fips():
    with open( fips_file_2010, newline='' ) as fips_file:
        reader = csv.reader(fips_file)
        for row in reader:

            state, fips_state, fips_county, county_name, class_code = row
            if state not in helpers.ALL_US_STATES: continue # skip AS, GU, MP, VI, PR, UM
            full_fips = fips_state + fips_county
            myfips = Fips(county_name, state, fips_state, fips_county)
            fips_2010[full_fips] = myfips

    return fips_2010

def build_2020_fips():
    wb = openpyxl.load_workbook(fips_file_2020)
    ws = wb['all-geocodes-v2019']
    for row in ws.iter_rows(min_row=6, values_only=True):

        fips_state = row[1]
        fips_county = row[2]
        county_name = row[6]
        state_abbr = helpers.FIPS_US_STATE.get(fips_state, False)

        if state_abbr not in helpers.ALL_US_STATES or fips_county == '000': continue # skip AS, GU, MP, VI, PR, UM
        myfips = Fips(county_name, state_abbr, fips_state, fips_county)
        full_fips = fips_state + fips_county
        fips_2020[full_fips] = myfips

    return fips_2020

# this is a list of fips which appeared in 2010 and went missing in 2020
changed_fips = fips_2010 - fips_2020 # {'51515', '02261', '02270', '46113'}
# 02261 - the old Valdez-Cordova CDP. Now it has split into 2 additional CDPs:
#   - 02063 Chugach Census Area
#   - 02066 Copper River Census Area
# 02270 - old Wade Hampton Census Area - renamed to Kusilvak Census Area and given new fips 02158. Nothing else changed.
# 46113 - old Shannon County - renamed to Oglala Lakota County and given new fips 46102. No other changes
# 51515 - old Bedford City, merged into Bedford County 51019

new_fips = fips_2020 - fips_2010 # {'02066', '02158', '02063', '46102'} # all new fips have already been accounted for.

### new adjacencies ###
# 02063 -   02063 Chugach
#           02020 Anchorage
#           02122 Kenai
#           02066 Copper River
#           02282 Yukatat
#           02170 Manatuska-Susitna
# 02066 -   02066 Copper River
#           02240 Southeast Fairbanks
#           02170 Manatuska-Susitna
#           02063 Chugach
#           02282 Yukatat
# 02261 - ignore all entries in the adjacency file (valdez-cordova was split into 2)
# 02270 - map all to 02158
# 46113 - map all to 46102
# 51515 - map all to 51019

# per the report, the following additional changes need to be made:
## add edges:
# 02105 Hoonah-Angoon -         02198 Prince of Wales-Hyder
# 02198 Prince of Wales-Hyder - 02220 Sitka
# 02195 Petersburg -            02110 Juneau
## remove edges:
# 02220 Sitka -                 02195 Petersburg
