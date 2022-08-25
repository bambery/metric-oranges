from classes.uid import Uid
from classes.fips import Fips
from classes.cbsa import Cbsa
from classes.airport import Airport

def process_fips_for_uid():
    for [fips_code, fips] in Fips.collection.items():
        if fips.cbsa_code == None:
            uid = Uid("FIPS")
            uid.airports.union(fips.airports)
        else:
            cbsa = Cbsa.collection[fips.cbsa_code]
            uid = Uid("CBSA")
            uid.airports.union(cbsa.airports)
            # associate CBSA with UID 
            cbsa.uid = uid.code

        uid.cbsa_codes.add(fips.cbsa_code)
        uid.fips_codes.add(fips_code)
        # associate the FIPS with the UID
        fips.uid = uid.code

        # associate airports with a uid
        for airport in uid.airports:
            Airport.collection[airport].uid = uid.code

        # collect the uid for safekeeping
        Uid.collection[uid.code] = uid
