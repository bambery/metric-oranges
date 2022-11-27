import csv

from classes.fips import Fips
from classes.uid import Uid

import shared.helpers as helpers
import shared.utils as utils

inputs = utils.get_inputs_dir()

dir_weekly = inputs.joinpath("jhu", "weekly_us")
dir_weekly_test = inputs.joinpath("jhu", "testing")

## deaths on UID

def count_deaths_by_uid():
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
                uid_code = Fips.get_uid_code(fips)
                Uid.add_deaths(uid_code, week_name, deaths)

## deaths on Week
