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

# I found a 2020 population by county with FIPS file, too late, which would be better to read in to get all county pops, to replace this little process. Alas.
# See contents.txt in /inputs/census/ or the 2020 pop file at /inputs/population_census_US/co-est2020.csv
ut_hd_fips, ut_hd_populations = uea.process_files()
ma_hd_fips = {'Dukes and Nantucket': {'25007': 20600, '25019': 14255 }}
ma_hd_populations = {'Dukes and Nantucket': 34855 }
ak_hd_fips = {'Bristol Bay plus Lake and Peninsula': {'02060': 838, '02164': 1416 }}
ak_hd_populations = {'Bristol Bay plus Lake and Peninsula': 2254}

def hamilton(hd, deaths, hd_fips, hd_populations):
    # Hamilton's Method
    fips = None
    # even if no deaths this week, still need to add zero entries for this date in the contained fips
    if deaths == 0:
        county_deaths = {}
        for fips in hd_fips[hd].keys():
            county_deaths[fips] = 0
        return county_deaths

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

# dates must be passed in as strings in the format of YYYY-MM-DD
def create_weekly_counts(start_date_str = "2020-10-01", end_date_str = "2022-08-01"):
    def determine_start_end_date(start_str, end_str):
        start_date = pen.from_format(start_str, "YYYY-MM-DD")
        prev_day = start_date.subtract(days=1)
        earliest_date = pen.from_format('2020-01-01', 'YYYY-MM-DD')
        if prev_day <= earliest_date:
            raise Exception("The start date is too far in the past. Choose a start date after 2022-01-01. Try 2020-01-02.")

        end_date = pen.from_format(end_str, "YYYY-MM-DD")

        # If the passed in start date is not a Sunday, begin generating reports on the next closest Sunday.
        if not start_date.day_of_week == pen.SUNDAY:
            start_date = start_date.next(pen.SUNDAY)

        # if the passed in end date is a Saturday, assume that is the end of the final week desired
        if end_date.day_of_week == pen.SATURDAY:
            end_date = end_date.next(pen.SUNDAY)
        # if end_date is any day of the week other than Sunday or Saturday, set the previous sunday as the cutoff.
        elif not end_date.day_of_week == pen.SUNDAY:
            end_date = end_date.previous(pen.SUNDAY)

        return [start_date, end_date]

    def for_key(pen):
        return pen.format("M/D/YY")

    # populates Node death counts
    # this is the method to adjust if you wish to attach deaths to FIPS or another data structure, or by a different period other than week
    def assign_to_node(start_date, end_date, node_deaths_dict):
        week_start = start_date
        week_end = week_start.next(pen.SUNDAY)
        while (week_start < end_date):

            count_start = int(row[ for_key(week_start) ])
            count_end = int(row[ for_key(week_end) ])
            # note: sometimes a week will have a net negative death total.
            # https://github.com/CSSEGISandData/COVID-19/issues/6250
            # this is fine.
            week_count = count_end - count_start

           # node = Node.get_by_fips(fips_code)
            date_key = week_start.format('YY-MM-DD')
            curr_deaths = node_deaths_dict.setdefault(date_key, 0)
            node_deaths_dict[date_key] = curr_deaths + week_count
            week_count = 0
            week_start = week_end
            week_end = week_start.next(pen.SUNDAY)
    ###########

    [start_date_x, end_date_x] = determine_start_end_date(start_date_str, end_date_str)

    if os.path.exists(file_jhu_time_series):
        with open(file_jhu_time_series, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                fips_code = helpers.format_fips(row['FIPS'].split('.')[0]) if row['FIPS'] else ''
                county_name = row['Admin2']
                country_name = row['iso2']
                state = row['Province_State']

                if (country_name != 'US'
                        or state.upper() not in helpers.US_STATES.keys()
                        or county_name.startswith('Unassigned')
                        or county_name.startswith("Out of")
                        or fips_code == '02261'):
                    continue

                curr_hd_fips = None
                curr_hd_populations = None
                # 02164 is "Bristol Bay plus Lake and Penninsula"
                if fips_code == '02164' or not fips_code:
                    # Kansas City mostly lies in Jackson County. This will get swept up by the "Kansas City, MO-KS" CBSA: 28140, in addition to the other counties that contain Kansas City.
                    if state == "Missouri" and county_name == "Kansas City":
                        fips_code = '29095'
                    elif state == "Utah" and county_name in ut_hd_fips.keys():
                        fips_code = '00000'
                        ##### temporary
                        curr_hd_fips = ut_hd_fips
                        curr_hd_populations = ut_hd_populations
                    elif state == "Massachusetts" and county_name == "Dukes and Nantucket":
                        fips_code = '00000'
                        ###### temporary
                        continue
                        curr_hd_fips = {'Dukes and Nantucket': {'25007': 20600, '25019': 14255 }}
                        curr_hd_populations = {'Dukes and Nantucket': 34855 }
                    elif state == "Alaska" and county_name == 'Bristol Bay plus Lake and Peninsula':
                        fips_code == '00000'
                        curr_hd_fips = ak_hd_fips
                        curr_hd_populations = ak_hd_populations
                    else:
                        continue

                if fips_code == "00000":
                    node_deaths = {}
                    assign_to_node(start_date_x, end_date_x, node_deaths)

                    week_name = None
                    d_count = None
                    for week_name, d_count in node_deaths.items():
                        deaths_to_add = hamilton(county_name, d_count, curr_hd_fips, curr_hd_populations)
                        fips = None
                        count = None
                        for fips, count in deaths_to_add.items():
                            actual_node = Node.get_by_fips(fips)
                            new_tot = actual_node.deaths.get( week_name, 0 ) + int(count)
                            actual_node.deaths[week_name] = new_tot
                else:
                    node_deaths = Node.get_by_fips(fips_code).deaths
                    assign_to_node(start_date_x, end_date_x, node_deaths)
