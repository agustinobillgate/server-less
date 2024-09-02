from functions.additional_functions import *
import decimal
from models import Parameters

def if_country_add_zonelistbl(cost_list_zone:str, s:str):
    rec_id = 0
    parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_id, parameters


        return {"rec_id": rec_id}

    parameters = Parameters()
    db_session.add(parameters)

    parameters.progname = "interface"
    parameters.section = "Dcode"
    parameters.varname = cost_list_zone
    parameters.vtype = 1
    parameters.vstring = s

    parameters = db_session.query(Parameters).first()
    rec_id = parameters._recid

    return generate_output()