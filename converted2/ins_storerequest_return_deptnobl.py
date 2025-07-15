#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def ins_storerequest_return_deptnobl(deptno:int):

    prepare_cache ([Parameters])

    parameters_vstring = ""
    avail_parameters = False
    parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters_vstring, avail_parameters, parameters
        nonlocal deptno

        return {"parameters_vstring": parameters_vstring, "avail_parameters": avail_parameters}


    parameters = db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == deptno)).first()

    if parameters:
        avail_parameters = True
        parameters_vstring = parameters.vstring

    return generate_output()