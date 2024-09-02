from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Parameters

def e1_main1_run_foreportbl(reportnr:int):
    avail_param = False
    parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_param, parameters


        return {"avail_param": avail_param}


    parameters = db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "FO_macro") &  (Parameters.SECTION == to_string(reportnr))).first()

    if parameters:
        avail_param = True

    return generate_output()