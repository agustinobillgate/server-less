#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def if_country_update_zonelistbl(zone_list_rec_id:int, city1:string, acode1:string):

    prepare_cache ([Parameters])

    parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters
        nonlocal zone_list_rec_id, city1, acode1

        return {}

    def update_zonelist():

        nonlocal parameters
        nonlocal zone_list_rec_id, city1, acode1

        s:string = ""

        parameters = get_cache (Parameters, {"_recid": [(eq, zone_list_rec_id)]})

        if parameters:
            pass
            parameters.vstring = city1 + ";" + acode1 + ";"
            pass
            pass


    update_zonelist()

    return generate_output()