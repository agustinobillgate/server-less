from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Parameters

def if_country_btn_delbl(case_type:int, cost_list_rec_id:int, last_zone:str):
    parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters


        return {}


    if case_type == 1:

        parameters = db_session.query(Parameters).filter(
                (Parameters._recid == cost_list_rec_id)).first()
        db_session.delete(parameters)

    elif case_type == 2:

        for parameters in db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "if_internal") &  (func.lower(Parameters.section) == "zone") &  (func.lower(Parameters.varname) == (last_zone).lower())).all():
            db_session.delete(parameters)

    return generate_output()