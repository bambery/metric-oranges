import csv

import shared.utils as utils
import shared.helpers as helpers

from classes.node import Node
from classes.fips import Fips
from classes.cbsa import Cbsa
from classes.airport import Airport

outputs = utils.get_outputs_dir()
file_path_airport_output = outputs.joinpath("airports.csv")
file_path_airport_edges_output = outputs.joinpath("airport_edges.csv")

def generate_airport_report():
    with open(file_path_airport_output, 'w', newline='') as csvout:
        writer = csv.writer(csvout)
        for locid, airport in Airport.collection.items():
            new_row = []
            new_row[0] = airport.locid
            new_row[1] = airport.name
            new_row[2] = airport.city
            new_row[3] = airport.state
            new_row[4] = airport.hub
            new_row[5] = airport.cbsa_code
            new_row[6] = airport.fips_code
            new_row[7] = airport.node_id

            writer.writerow(new_row)

def generate_airport_edges():




