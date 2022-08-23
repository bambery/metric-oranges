import pandas as pd
#local imports
import shared.utils as utils
import shared.helpers as helpers
from classes.airport import Airport
from classes.fips import Fips
from classes.cbsa import Cbsa

inputs = utils.get_inputs_dir()

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', None)

file_path_airports = inputs.joinpath("faa", "NPIAS", "NPIAS-Report-2017-2021-Appendix-A.xlsx")

def process_airports(place_cbsa):
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
        return {key for key in place_cbsa.keys() if key.startswith(state)}


    for row in mycsv.splitlines():
        state, city, airport_name, locid, hub, enplaned = row.split(",")

        if len(hub) == 0: continue # ignore row if hub is empty
        if state not in helpers.ALL_US_STATES:
            continue # ignore non US States

        if city.startswith("St."): # St vs St. is very inconsistent
            city = "St" + city.removeprefix("St.")

        if city == "Grand Canyon" and state == "AZ": # this is actually located in Tusayan CDP and is part of the Flagstaff CBA
            city = "Tusayan"
#            cbsa = '22380'
#            fips = '04005'
        elif city == "St Petersburg-Clearwater" and state == "FL": # there are 2 airports in St Petersburg and this one gets a more specific name
            city = "St Petersburg"
            #cbsa = '45300'
            #fips = '12103'
        elif city == "Augusta" and state == "GA": # this is a colloquial name, the full name is Augusta-Richmond County
            city = "Augusta-Richmond County"
            #cbsa = 12260
            #fips = 13245
        elif city == "Boise" and state == "ID":
            city = "Boise City"
        elif city == "Hyannis": # named after a business district
            city = "Barnstable Town"
        elif city == "Iron Mountain Kingsford":
            city = "Iron Mountain"
        elif city == "Block Island":
            continue # I have chosen to skip this airport. It is a non-hub on a small island off of RI
        elif city == "Dallas-Fort Worth":
            city = "Dallas" # will get captured by the Dallas-Fort Worth-Arlington CBSA


        if city == "Deadhorse":
            cbsa_code = None
            fips_code = '02185'
        else:
            lookup = place_cbsa.get( state + "_" + city.upper())
            cbsa_code = lookup["cbsa"]
            fips_code = lookup["fips"]

        # the place mapping was from 2006, and no more recent version was available after Trump gutted the Census: numerous reports that were available as of 2018 are all missing. There are some updates that need to be made:
        # two airports are located in FIPS that are no longer associated with CBSAs
        if cbsa_code == "28980": # locid: AQD
            cbsa_code = None # does not exist, no record
            fips_code = "02150" # Kodak Island Borough
        elif cbsa_code == "40500": # locid: RKD, Rockland, ME airport - no longer in a CBSA
            cbsa_code = None

        # updates to changed CBSAs
        if cbsa_code:
            if cbsa_code == "31100": # old cali cbsa
                cbsa_code = "31080" # current Los Angeles-Long Beach-Anaheim CBSA
                if locid in ["BUR", "LGB"]: 
                    fips_code = "06037" # Los Angeles County, where this airport resides
                if locid in ["LAX"]:
                    fips_code = "06059" # Los Angeles County, where this airport resides
            elif cbsa_code == "42060": # locid: SBA. Apparently Santa Barbara has changed
                cbsa_code = "42200"
            elif cbsa_code == "42260": # locid: SRQ, old Sarasota CBSA, FL
                cbsa_code = "35840"
            elif cbsa_code == "23020": # locid: VPS, old Fort Walton CBSA
                cbsa_code = "18880"
            elif cbsa_code == "26180": # locid: HNL, old Honolulu CBSA
                cbsa_code = "46520"
            elif cbsa_code == "14060": # locid: BMI, old Bloomington, IL CBSA 
                cbsa_code = "14010" 
            elif cbsa_code == "30100": # locid: LEB, Lebanon, NH - old CBSA code
                cbsa_code = "17200"
            elif cbsa_code == "39100": # locid: SWF, NewYork Orange County - old CBSA
                cbsa_code = "35620"

            Cbsa.collection[cbsa_code]
            Cbsa.collection[cbsa_code].airports.add(locid)
        else:
            Fips.collection[fips_code].airports.add(fips_code)

        myairport = Airport(airport_name, state, city, locid, hub, enplaned, cbsa_code, fips_code)
        Airport.collection[locid] = myairport

    print("u made it!!!!!")
