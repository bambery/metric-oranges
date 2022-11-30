import csv
import openpyxl
import os

from classes.fips import Fips
from classes.node import Node

import shared.helpers as helpers
import shared.utils as utils

inputs = utils.get_inputs_dir()

dir_weekly = inputs.joinpath("jhu", "weekly_us")

# deaths will be saved on Node


def count_deaths_by_node(test=False):

    # populates Node death counts
    # this is the method to adjust if you wish to attach deaths to FIPS or another data structure
    def count_deaths(weekly_dir):

        for weekly_deaths in weekly_dir.iterdir():
            with open(weekly_deaths) as file:
                week_name = weekly_deaths.stem
                reader = csv.reader(file)
                for row in reader:
                    fips = row[0]
                    deaths = row[1]

                    # there are zombie entries for defunct FIPS which always have 0 deaths. Skip these, and any other zero death entries.
                    if int(deaths) == 0:
                        continue
                    node_id = Fips.get_node_id(fips)
                    Node.add_deaths(node_id, week_name, deaths)

    # if spot checking, control which files to examine here
    if test:
        import shutil
        dir_weekly_test = inputs.joinpath("jhu", "testing")
        if os.path.isdir(dir_weekly_test):
            shutil.rmtree(dir_weekly_test)
        os.mkdir(dir_weekly_test)

        weeklies = sorted(os.listdir(dir_weekly))
        three = weeklies[0:3]
        for filename in three:
            shutil.copy
            source = inputs.joinpath(dir_weekly, filename)
            dest = inputs.joinpath(dir_weekly_test, filename)
            shutil.copy(source, dest)

        count_deaths(dir_weekly_test)
    else:
        count_deaths(dir_weekly)
