import openpyxl
import csv
import shared.utils as utils

inputs = utils.get_inputs_dir()

file_path_utah_census = inputs.joinpath("census", "utah_2020_census", "co-est2021-pop-49.xlsx")
file_path_utah_health_dist = inputs.joinpath("utah_ibis", "Density.xlsx")
file_path_utah_fips_hd = inputs.joinpath("utah_ibis", "health_districts_fips.txt")

## Utah does not report deaths by FIPS, but instead by "health districts" which cover several counties.
# In order to produce data which is usefully comparable to other states, I will be apportioning the deaths among the counties in each health district using Hamilton's Method.
# https://www.ams.org/publicoutreach/feature-column/fcarc-apportionii1

county_to_hd = {}
hd_fips = {}
county_to_fips = {}
hd_populations = {}
fips_populations = {}

# scoping :( miss u so bad javascript
def process_files():
    def read_hd_fips():
        # get health dist to FIPS mapping
        with open(file_path_utah_fips_hd) as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0]: # if there is an entry in col 1, then this is begins a new health district
                    h_dist = row[0]
                    hd_fips[h_dist] = {}
                else:
                    fips_code = row[1]
                    county_name = row[2]

                    county_to_hd[county_name] = h_dist
                    hd_fips[h_dist][fips_code] = 0
                    county_to_fips[county_name] = fips_code

    def read_utah_pop():
        # get county populations
        wb = openpyxl.load_workbook(file_path_utah_census)
        ws = wb['CO-EST2021-POP-49']
        for row in ws.iter_rows(min_row=5, max_row=34, values_only=True):
            area_name = row[0].split(',')[0].lstrip('.')
            if area_name not in county_to_hd.keys(): continue

            county_population = row[1]
            fips_code = county_to_fips[area_name]
            hd = county_to_hd[area_name]

            hd_pop = hd_populations.setdefault(hd, 0)
            hd_populations[hd] = hd_pop + county_population
            fips_populations[fips_code] = county_population
            hd_fips[hd][fips_code] = county_population
    read_hd_fips()
    read_utah_pop()
    # sort fips by largest pop
    for hd, fips in hd_fips.items():
        fips = dict(sorted(fips.items(), key=lambda x:x[1]))

    return [hd_fips, hd_populations]
