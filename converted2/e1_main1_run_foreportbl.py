#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def e1_main1_run_foreportbl(reportnr:int):
    avail_param = False
    parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_param, parameters
        nonlocal reportnr

        return {"avail_param": avail_param}


    parameters = get_cache (Parameters, {"progname": [(eq, "fo-macro")],"section": [(eq, to_string(reportnr))]})

    if parameters:
        avail_param = True

    return generate_output()