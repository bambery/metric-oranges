import pandas as pd
import shared.utils as utils
import shared.helpers as helpers
from classes.airport import Airport
from classes.fips import Fips
from classes.cbsa import Cbsa

inputs = utils.get_inputs_dir()

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', None)

file_path_airports = inputs.joinpath("faa", "NPIAS", "NPIAS-Report-2017-2021-Appendix-A.xlsx")

def process_airports(place_cbsa_lookup):

    # local helpers
    ###############
    def clean_name(str):
        if str.find(",") > -1:
            str = str.split(",", maxsplit =1)[0]
        if str.find("/") > -1:
            str = str.split("/", maxsplit=1)[0]
        return str

    def convert_airports_to_csv():
        airports = pd.read_excel(
                file_path_airports,
                sheet_name = "All NPIAS Airports",
                skiprows = 3,
                skipfooter = 1,
                usecols = [0, 1, 2, 3, 5, 9],
                names = ["State", "City", "Name", "LOCID", "Hub", "Enplaned (2017-2021)"],
                converters={'City': clean_name, 'Name': clean_name }
                )
        # optionally, write to temp file and read back in line by line
        return airports.to_csv(None, index = False, header = False)
    mycsv = convert_airports_to_csv()

    def state_places(state):
        return {key for key in place_cbsa_lookup.keys() if key.startswith(state)}

    # process input file
    ####################
    for row in mycsv.splitlines():
        state, city, airport_name, locid, hub, enplaned = row.split(",")

        if len(hub) == 0: continue # ignore row if hub is empty
        if state not in helpers.ALL_US_STATES:
            continue # ignore non US States

        if city.startswith("St."): # St vs St. is very inconsistent
            city = "St" + city.removeprefix("St.")

        ### the names of the "cities" the airports are located in are sometimes not the actual city names and must be corrected ###
        if city == "Grand Canyon" and state == "AZ": # this is actually located in Tusayan CDP and is part of the Flagstaff CBA
            city = "Tusayan"
        elif city == "St Petersburg-Clearwater" and state == "FL": # there are 2 airports in St Petersburg and this one gets a more specific name
            city = "St Petersburg"
        elif city == "Augusta" and state == "GA": # this is a colloquial name, the full name is Augusta-Richmond County
            city = "Augusta-Richmond County"
        elif city == "Boise" and state == "ID":
            city = "Boise City"
        elif city == "Hyannis" and state == "MA":# named after a business district
            city = "Barnstable Town"
        elif city == "Iron Mountain Kingsford" and state == "MI": # local name
            city = "Iron Mountain"
        elif city == "Block Island" and state == "RI":
            continue # I have chosen to skip this airport. It is a non-hub on a small island off of RI
        elif city == "Dallas-Fort Worth":
            city = "Dallas" # will get captured by the Dallas-Fort Worth-Arlington CBSA
        elif city == "St Mary'S" and state == "AK": # typo in report
            city = "St Mary's"

        # Deadhorse does not appear in the places file
        if city == "Deadhorse":
            cbsa_code = None
            fips_code = '02185'
        else:
            place = place_cbsa_lookup.get( state + "_" + city.upper())
            cbsa_code = place["cbsa"]
            fips_code = place["fips"]

        # the place mapping was from 2006, and no more recent version was available after Trump gutted the Census: numerous reports that were available as of 2018 are all missing. There are some updates that need to be made to conform to 2020 standards:

        # two airports are located in FIPS that are no longer associated with CBSAs
        if cbsa_code == "28980": # locid: AQD
            cbsa_code = None # does not exist, no record
            fips_code = "02150" # Kodak Island Borough
        elif cbsa_code == "40500": # locid: RKD, Rockland, ME airport - no longer in a CBSA
            cbsa_code = None

        # updates to changed FIPS
        if fips_code:
            if fips_code == "02280":
                fips_code = "02195" # changed to Petersburg Borough, AK
                cbsa_code = None
           # old CDP Valdez-Cordova split into 2 CDPs
            if fips_code == "02261" and locid == "VDZ":
                fips_code = "02063" # now located in Chugach CDP
                cbsa_code = None
            if fips_code == "02261" and locid == "CDV":
                fips_code = "02063" # also located in Chugach CDP
                cbsa_code = None
            if fips_code == "02270" and locid == "KSM": # changed to Kusilvak CDP
                fips_code = "02158"
                cbsa_code = None
#
#        # updates to changed CBSAs
        if cbsa_code:
            if cbsa_code == "31100": # old cali cbsa
                cbsa_code = "31080" # current Los Angeles-Long Beach-Anaheim CBSA
                if locid in ["BUR", "LGB"]:
                    fips_code = "06037" # Los Angeles County, where this airport resides
                if locid in ["LAX"]:
                    fips_code = "06059" # Orange County, where this airport resides
            elif cbsa_code == "42060":  # locid: SBA. This CBSA has changed over time
                cbsa_code = "42200"
            elif cbsa_code == "42260":  # locid: SRQ, old Sarasota CBSA, FL
                cbsa_code = "35840"
            elif cbsa_code == "23020":  # locid: VPS, old Fort Walton CBSA
                cbsa_code = "18880"
            elif cbsa_code == "26180":  # locid: HNL, old Honolulu CBSA
                cbsa_code = "46520"
            elif cbsa_code == "14060":  # locid: BMI, old Bloomington, IL CBSA
                cbsa_code = "14010"
            elif cbsa_code == "19380":  # locid: DAY, Dayton, OH CBSA has expanded
                cbsa_code = "19430"

            # associate CBSA with this airport
            ##################################
            Cbsa.collection[cbsa_code].airports.add(locid)
        else:
            # associate fips with this airport
            ##################################
            # - note that ONLY fips who do NOT belong to a CBSA have airports directly associated with them
            # - the Airport object remains aware of both CBSA and FIPS
            Fips.collection[fips_code].airports.add(locid)

        # create airport object
        #######################
        myairport = Airport(airport_name, state, city, locid, hub, enplaned, cbsa_code, fips_code)
