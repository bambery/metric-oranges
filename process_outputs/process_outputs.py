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
file_path_cbsa_output = outputs.joinpath("cbsa.csv")
file_path_fips_output = outputs.joinpath("fips.csv")
file_path_node_output = outputs.joinpath("nodes.csv")
file_path_node_covid_output = outputs.joinpath("weekly_covid_by_node.csv")

def generate_airport_report():
    with open(file_path_airport_output, 'w', newline='') as csvout:
        writer = csv.writer(csvout)
        header = ["LOCID", "Node ID", "Airport Name", "City", "State", "NPIAS Hub Designation", "CBSA Code", "FIPS Code", "Destinations"]
        writer.writerow(header)
        for locid, airport in Airport.collection.items():
            new_row = []
            new_row.append(airport.locid)
            new_row.append(airport.node_id)
            new_row.append(airport.name)
            new_row.append(airport.city)
            new_row.append(airport.state)
            new_row.append(airport.hub)
            new_row.append(airport.cbsa_code)
            new_row.append(airport.fips_code)
            new_row.append("|".join(airport.destinations))

            writer.writerow(new_row)

def generate_airport_edge_report():
    with open(file_path_airport_edges_output, 'w', newline='') as csvout:
        writer = csv.writer(csvout)
        header = ["LOCID Origin", "LOCID Destination"]
        writer.writerow(header)
        for locid, airport in Airport.collection.items():
            for dest in airport.destinations:
                new_row = []
                new_row.append(locid)
                new_row.append(dest)

                writer.writerow(new_row)

def generate_cbsa_report():
    with open(file_path_cbsa_output, 'w', newline='') as csvout:
        writer = csv.writer(csvout)
        header = ["CBSA Code", "Node ID", "Name", "MSA Designation", "Airports", "FIPS Codes"]
        writer.writerow(header)
        for code, cbsa in Cbsa.collection.items():
            new_row = []
            new_row.append(code)
            new_row.append(cbsa.node_id)
            new_row.append(cbsa.name)
            new_row.append(cbsa.msa_designation)
            new_row.append("|".join(cbsa.airports))
            new_row.append("|".join(cbsa.fips_codes))

            writer.writerow(new_row)

def generate_fips_report():
    with open(file_path_fips_output, 'w', newline='') as csvout:
        writer = csv.writer(csvout)
        header = ["FIPS Code", "Node ID", "Name", "State", "CBSA Code", "Airports", "Adjacent FIPS Codes", "Adjacent Node IDs"]
        writer.writerow(header)
        for code, fips in Fips.collection.items():
                new_row = []
                new_row.append(code)
                new_row.append(fips.node_id)
                new_row.append(fips.county)
                new_row.append(fips.state)
                new_row.append(fips.cbsa_code)
                new_row.append("|".join(fips.airports))
                new_row.append("|".join(fips.adjacent_fips_codes))
                new_row.append("|".join(fips.adjacent_node_ids))

                writer.writerow(new_row)

def generate_node_report():
    with open(file_path_node_output, 'w', newline='') as csvout:
        writer = csv.writer(csvout)
        header = ["Node ID", "Name", "CBSA Code", "FIPS Codes", "Airports", "Edge Node IDs (All)", "Edge Nodes by Geographic Adjacency", "Edge Nodes by Flight"]
        writer.writerow(header)
        for nodeid, node in Node.collection.items():
                new_row = []
                new_row.append(node.id_)
                new_row.append(node.name)
                new_row.append(node.cbsa_code)
                new_row.append("|".join(node.fips_codes))
                new_row.append("|".join(node.airports))
                new_row.append("|".join(node.edges()))
                new_row.append("|".join(node.edges_adjacent))
                new_row.append("|".join(node.edges_flights))

                writer.writerow(new_row)

def generate_node_covid_report():
    with open(file_path_node_covid_output, 'w', newline='') as csvout:
        writer = csv.writer(csvout)
        header = ["Node ID", "Week Start", "Deaths Recorded For Week"]
        writer.writerow(header)
        for nodeid, node in Node.collection.items():
            for date, deaths in node.deaths.items():
                new_row = []
                new_row.append(nodeid)
                new_row.append(date)
                new_row.append(deaths)

                writer.writerow(new_row)
