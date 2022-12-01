# this script first runs through the JHU daily files, and writes to the file system new weekly files that are stripped of everything except FIPS and the weekly death count for US counties

import csv
import os
import math
import pendulum as pen
import pandas as pd

import shared.utils as utils
import shared.helpers as helpers
import process_inputs.utah_et_al as uea

from classes.node import Node

inputs = utils.get_inputs_dir()

file_jhu_time_series = inputs.joinpath("jhu", "COVID-19", "csse_covid_19_data", "csse_covid_19_time_series", "time_series_covid19_deaths_US.csv")

#dir_jhu_inputs = inputs.joinpath("jhu", "COVID-19", "csse_covid_19_data", "csse_covid_19_daily_reports")
#dir_jhu_destination = inputs.joinpath("jhu", "weekly_us")

def hamilton(hd, deaths, hd_fips, hd_populations):
    # Hamilton's Method
    ## calculate the divisor for the HD
    divisor = hd_populations[hd]/deaths
    remaining = deaths
    county_quotas = {}
    county_deaths = {}
    quota_remainders = {}

    ## determine each county's quota
    fips = None
    for fips in hd_fips[hd].keys():
        county_quotas[fips] = hd_fips[hd][fips]/divisor

    # distribute the whole number deaths
    fips = None
    quotas = None
    for fips, quotas in county_quotas.items():
        county_deaths[fips] = math.floor(quotas)

    fips = None
    quota = None
    num = None
    remaining = remaining - sum([ math.floor(num) for num in county_quotas.values() ])
    quota_remainders = { fips: quota % 1 for fips, quota in county_quotas.items() }

    # sort quota remainders by largest
    fips_by_quota_desc = utils.sort_dict_by_val_desc(quota_remainders)

    fips = None
    for fips in fips_by_quota_desc.keys():
        if remaining > 0:
            if fips not in county_deaths:
                county_deaths[fips] = 1
            else:
                county_deaths[fips] = county_deaths[fips] + 1

            remaining = remaining - 1
    if remaining > 0:
        raise Exception("You messed up somehow, and did not distibute enough deaths.")

    return county_deaths


# format of daily jhu input files:
# 0: fips, 1: county name, 2: state name, 3: country abbreviated, 4: not used, 5: lat, 6: long, 7: confirmed cases, 8: deaths, 9: recovered (not used), 10: active (not used), 11: combined_key, 12: incident rate, 13: case fatality ratio

# dates must be passed in as strings in the format of YYYY-MM-DD
def create_weekly_reports(start_date_str, end_date_str):
    # delete old reports and create a fresh directory

    ut_hd_fips, ut_hd_populations = uea.process_files()
    ma_hd_fips = {'Dukes and Nantucket': {'25007': 20600, '25019': 14255 }}
    ma_hd_populations = {'Dukes and Nantucket': 34855 }

    start_date = pen.from_format(start_date_str, "YYYY-MM-DD")
    prev_day = start_date.subtract(days=1)
    earliest_date = pen.from_format('2020-01-01', 'YYYY-MM-DD')
    if prev_day <= earliest_date:
        raise Exception("The start date is too far in the past. Choose a start date after 2022-01-01. Try 2020-01-02.")

    end_date = pen.from_format(end_date_str, "YYYY-MM-DD")

    # If the passed in start date is not a Sunday, begin generating reports on the next closest Sunday.
    if not start_date.day_of_week == pen.SUNDAY:
        week_start = start_date.next(pen.SUNDAY)

    # if the passed in end date is a Saturday, assume that is the end of the final week desired
    if end_date.day_of_week == pen.SATURDAY:
        end_date = end_date.next(pen.SUNDAY)
    # if end_date is any day of the week other than Sunday or Saturday, set the previous sunday as the cutoff.
    elif not end_date.day_of_week == pen.SUNDAY:
        end_date = end_date.previous(pen.SUNDAY)

    curr_date = week_start
    week_end = week_start.next(pen.SUNDAY)
    week_counts = {}

    csv.

    while (curr_date < end_date):
        # generate weekly report
        if (curr_date == week_end):
            # output weekly report
            df = pd.DataFrame.from_dict(week_counts, orient='index')
            df.to_csv(output_file, header=False)
            df = None

            # reset weekly vars
            week_counts = {}
            week_start = week_end
            week_end = week_start.next(pen.SUNDAY)

        daily_file = dir_jhu_inputs / toJhuFilenameStr(curr_date)

        if os.path.exists(daily_file):
            with open(daily_file) as file:
                reader = csv.reader(file, delimiter=",")
                header = next(reader)

                # if fips and "county" name are not blank, county is not "unassigned" or begins with "Out of", and not a territory
                row = None
                for row in reader:
                    fips_raw = row[0]
                    county_name = row[1]
                    state = row[2]
                    country = row[3]
                    deaths = int(row[8]) if row[8] != '' else 0
                    fips_code = None

                    if county_name and country == "US" and county_name != "Unassigned" and not county_name.startswith("Out of") and state.upper() in helpers.US_STATES.keys():
                        if fips_raw:
                            fips_code = helpers.format_fips(fips_raw)
                        elif country == "US" and not fips_raw and state == "Missouri" and county_name == "Kansas City":
                            # Kansas City mostly lies in Jackson County. This will get swept up by the "Kansas City, MO-KS" CBSA: 28140, in addition to the other counties that contain Kansas City.
                            fips_code = '29095'

                        if fips_code:
                            new_tot = week_counts.get( fips_code, 0 ) + int(deaths)
                            week_counts[ fips_code ]= new_tot
                        elif not fips_raw and state == "Massachusetts" and county_name == "Dukes and Nantucket":
                            # accomodate Dukes/Nantucket
                            deaths_to_add = hamilton(county_name, deaths, ma_hd_fips, ma_hd_populations)
                            fips = None
                            count = None
                            for fips, count in deaths_to_add.items():
                                new_tot = week_counts.get( fips, 0 ) + int(count)
                                week_counts[ fips ] = new_tot

                        elif not fips_raw and state == "Utah":
                            # distribute Utah health dept deaths among counties
                            deaths_to_add = hamilton(county_name, deaths, ut_hd_fips, ut_hd_populations)
                            fips = None
                            count = None
                            for fips, count in deaths_to_add.items():
                                new_tot = week_counts.get( fips, 0 ) + int(count)
                                week_counts[ fips ] = new_tot

                curr_date = curr_date.add(days=1)
        else:
            raise Exception("trying to open file that doesn't exist: " + next_file)
            break
