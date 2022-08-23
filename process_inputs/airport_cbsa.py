import pandas as pd
#local imports
import shared.utils as utils
from classes.airport import Airport

inputs = utils.get_inputs_dir()

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', None)

file_path_airports = inputs.joinpath("faa", "NPIAS", "NPIAS-Report-2017-2021-Appendix-A.xlsx")

def process_airports():
    def convert_airports_to_csv():
        airports = pd.read_excel(
                file_path_airports,
                sheet_name = "All NPIAS Airports",
                skiprows = 1,
                skipfooter = 1,
                usecols = [0, 1, 2, 3, 5, 8],
                names = ["State", "City", "Name", "LOCID", "Hub", "Enplaned (2017-2021)"]
                )
        # optionally, write to temp file and read back in line by line
        return airports.to_csv(None, index = False, header = False)
    mycsv = convert_airports_to_csv()

    for row in mycsv.splitlines():
        breakpoint()
        # skip if enplaned = 0

