import pandas as pd
import shared.utils as utils
import shared.helpers as helpers
from classes.airport import Airport
from classes.fips import Fips
from classes.cbsa import Cbsa

inputs = utils.get_inputs_dir()

file_path_airports = inputs.joinpath("faa", "NPIAS", "NPIAS-Report-2017-2021-Appendix-A.xlsx")

def process_airports(place_cbsa_lookup):

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

    # process input file
    ####################
    row = None
    for row in mycsv.splitlines():
        fips_code = None
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

        # Deadhorse does not appear in the places file. It is in Kusilvak Census Area
        if city == "Deadhorse":
            cbsa_code = None
            fips_code = '02185'
        else:
            place = place_cbsa_lookup.get( state + "_" + city.upper())
            fips_code = place["fips"]
            if not fips_code:
                raise Exception("looking for somewhere that doesn't exist (in this ancient places file)")

        # the place mapping was from 2006, and no more recent version was available after Trump gutted the Census: numerous reports that were available as of 2018 are all missing. There are some updates that need to be made to conform to 2020 standards:

        # updates to changed FIPS
        if fips_code:
            if fips_code == "02280":
                fips_code = "02195" # changed to Petersburg Borough, AK
           # old CDP Valdez-Cordova split into 2 CDPs
            if fips_code == "02261" and locid == "VDZ":
                fips_code = "02063" # now located in Chugach CDP
            if fips_code == "02261" and locid == "CDV":
                fips_code = "02063" # also located in Chugach CDP
            if fips_code == "02270" and locid == "KSM": # changed to Kusilvak CDP
                fips_code = "02158"
#
            cbsa_code = Fips.get(fips_code).cbsa_code
            # - note that ONLY fips who do NOT belong to a CBSA have airports directly associated with them
            # the Airport remains aware of both FIPS and CBSA
        if cbsa_code:
            Cbsa.collection[cbsa_code].airports.add(locid)
        else:
            Fips.collection[fips_code].airports.add(locid)

        myairport = Airport(airport_name, state, city, locid, hub, enplaned, cbsa_code, fips_code)
        Airport.collection[locid] = myairport
