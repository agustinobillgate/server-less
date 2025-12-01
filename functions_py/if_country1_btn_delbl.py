#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def if_country1_btn_delbl(case_type:int, cost_list_rec_id:int, last_zone:string, ifname:string):
    parameters = None

    db_session = local_storage.db_session
    last_zone = last_zone.strip()
    ifname = ifname.strip()

    def generate_output():
        nonlocal parameters
        nonlocal case_type, cost_list_rec_id, last_zone, ifname

        return {}


    if case_type == 1:

        # parameters = get_cache (Parameters, {"_recid": [(eq, cost_list_rec_id)]})
        parameters = db_session.query(Parameters).filter(Parameters._recid == cost_list_rec_id).with_for_update().first()

        if parameters:
            pass
            db_session.delete(parameters)

    elif case_type == 2:

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("interface")) & (Parameters.section == ("zone")) & 
                 (Parameters.varname == (last_zone))).order_by(Parameters._recid).with_for_update().all():
            db_session.delete(parameters)

    elif case_type == 3:

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == (ifname)) & (Parameters.section == ("DCode")) & (Parameters.varname == (last_zone))).order_by(Parameters._recid).with_for_update().all():
            db_session.delete(parameters)

    return generate_output()