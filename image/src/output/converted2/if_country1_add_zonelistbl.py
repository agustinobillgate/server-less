#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def if_country1_add_zonelistbl(ifname:string, cost_list_zone:string, s:string):

    prepare_cache ([Parameters])

    rec_id = 0
    parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_id, parameters
        nonlocal ifname, cost_list_zone, s

        return {"rec_id": rec_id}

    def add_zonelist():

        nonlocal rec_id, parameters
        nonlocal ifname, cost_list_zone, s


        parameters = Parameters()
        db_session.add(parameters)

        parameters.progname = ifname
        parameters.section = "Dcode"
        parameters.varname = cost_list_zone
        parameters.vtype = 1
        parameters.vstring = s


        pass
        rec_id = parameters._recid


    add_zonelist()

    return generate_output()