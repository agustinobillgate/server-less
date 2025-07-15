#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def if_country_btn_delbl(case_type:int, cost_list_rec_id:int, last_zone:string):
    parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters
        nonlocal case_type, cost_list_rec_id, last_zone

        return {}


    if case_type == 1:

        parameters = get_cache (Parameters, {"_recid": [(eq, cost_list_rec_id)]})

        if parameters:
            pass
            db_session.delete(parameters)

    elif case_type == 2:

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("if-internal").lower()) & (Parameters.section == ("zone").lower()) & (Parameters.varname == (last_zone).lower())).order_by(Parameters._recid).all():
            db_session.delete(parameters)

    return generate_output()