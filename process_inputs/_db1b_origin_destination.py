# I am highly constrained in the files I have access to in order to attempt to cobble together this information. The files are too large for me to have stored at the same time, so in order to have useful inputs, I have processed all 4 quarters of the DB1BMarket for 2019, one quarter per output file, for easy reading in later.

# This file is run once

import csv
import os

import shared.utils as utils

inputs = utils.get_inputs_dir()
dest_dir = inputs.joinpath("bts", "origin_dest")

#file_path_db1b_2019_q1 = inputs.joinpath("bts", "Origin_and_Destination_Survey_DB1BMarket_2019_1.csv")
file_path_db1b_2019_q2 = inputs.joinpath("bts", "Origin_and_Destination_Survey_DB1BMarket_2019_2.csv")
#file_path_db1b_2019_q3 = inputs.joinpath("bts", "Origin_and_Destination_Survey_DB1BMarket_2019_3.csv")
#file_path_db1b_2019_q4 = inputs.joinpath("bts", "Origin_and_Destination_Survey_DB1BMarket_2019_4.csv")

# This output file is not directional, and it encompasses all lsted Airports, without checking if they are hub-rated.

def process_flight_edges(db1b_2019_quarter):
    quarterly_flights = set()

    with open(db1b_2019_quarter, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            route = []
            route.append(row["Origin"])
            route.append(row["Dest"])
            route_str = ":".join(sorted(route))
            quarterly_flights.add(route_str)

    dest_file = dest_dir.joinpath("db1b_origin_dest_q2.csv")
    with open(dest_file, 'w', newline='') as csvout:
        writer = csv.writer(csvout)
        for fr in sorted(quarterly_flights):
            writer.writerow(fr.split(":"))

def write_routes():
    process_flight_edges(file_path_db1b_2019_q2)
