import csv

from classes.fips import Fips
from classes.node import Node

import shared.helpers as helpers
import shared.utils as utils

inputs = utils.get_inputs_dir()

dir_weekly = inputs.joinpath("jhu", "weekly_us")
dir_weekly_test = inputs.joinpath("jhu", "testing")

## deaths will be saved on Node

def count_deaths_by_node():
    #for weekly_deaths in dir_weekly.iterdir():
    for weekly_deaths in dir_weekly_test.iterdir():
        print('inside weekly')
        with open(weekly_deaths) as file:
            week_name = weekly_deaths.stem
            print('reading file ' + week_name)
            reader = csv.reader(file)
            for row in reader:
                fips = row[0]
                deaths = row[1]

                # there are zombie entries for defunct FIPS which always have 0 deaths. Skip these, and any other zero death entries.
                if int(deaths) == 0:
                    continue
                node_id = Fips.get_node_id(fips)
                Node.add_deaths(node_id, week_name, deaths)

## deaths on Week
