import csv

import shared.helpers as helpers
import shared.utils as utils

from classes.airport import Airport

inputs = utils.get_inputs_dir()

file_path_db1b_2019_q3 = inputs.joinpath("bts", "Origin_and_Destination_Survey_DB1BMarket_2019_3.csv")

def process_flight_edges():
    with open(file_path_db1b_2019_q3, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            origin_locid = row["Origin"]
            dest_locid = row["Dest"]

            Airport.add_flight_route(origin_locid, dest_locid)
