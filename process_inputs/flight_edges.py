import csv

import shared.helpers as helpers
import shared.utils as utils

from classes.airport import Airport
from classes.node import Node

inputs = utils.get_inputs_dir()

file_path_flight_routes = inputs.joinpath("bts", "origin_dest", "2019_directionless_flight_routes.csv")

def process_flight_edges():
    with open(file_path_flight_routes, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            origin_locid = row[0]
            dest_locid = row[1]
            if origin_locid in Airport.collection.keys() and dest_locid in Airport.collection.keys():
                Airport.add_flight_route(origin_locid, dest_locid)

    assign_flight_edges_to_nodes()

def assign_flight_edges_to_nodes():
    for locid, airport in Airport.collection.items():
        if not airport.node_id:
            breakpoint()
        origin_airport_node = Node.get(airport.node_id)
        for dest_locid in airport.destinations:
            dest_airport_node_id = Airport.collection.get(dest_locid).node_id
            origin_airport_node.edges_flights.add(dest_airport_node_id)
