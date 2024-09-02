from functions.additional_functions import *
import decimal
from models import Parameters

def if_country1_add_zonelistbl(ifname:str, cost_list_zone:str, s:str):
    rec_id = 0
    parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_id, parameters


        return {"rec_id": rec_id}

    def add_zonelist():

        nonlocal rec_id, parameters


        parameters = Parameters()
        db_session.add(parameters)

        parameters.progname = ifname
        parameters.section = "Dcode"
        parameters.varname = cost_list_zone
        parameters.vtype = 1
        parameters.vstring = s

        parameters = db_session.query(Parameters).first()
        rec_id = parameters._recid

    add_zonelist()

    return generate_output()