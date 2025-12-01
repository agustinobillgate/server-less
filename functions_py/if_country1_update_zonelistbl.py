#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def if_country1_update_zonelistbl(zone_list_rec_id:int, city1:string, acode1:string, s:string):

    prepare_cache ([Parameters])

    parameters = None

    db_session = local_storage.db_session
    acode1 = acode1.strip()
    city1 = city1.strip()
    s = s.strip()

    def generate_output():
        nonlocal parameters
        nonlocal zone_list_rec_id, city1, acode1, s

        return {}

    def update_zonelist():

        nonlocal parameters
        nonlocal zone_list_rec_id, city1, acode1, s

        # parameters = get_cache (Parameters, {"_recid": [(eq, zone_list_rec_id)]})
        parameters = db_session.query(Parameters).filter(
                 (Parameters._recid == zone_list_rec_id)).with_for_update().first()

        if parameters:
            parameters.vstring = (f"{city1};{acode1};{s}")


    update_zonelist()

    return generate_output()