from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Parameters

def ins_storerequest_return_deptnobl(deptno:int):
    parameters_vstring = ""
    avail_parameters = False
    parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters_vstring, avail_parameters, parameters


        return {"parameters_vstring": parameters_vstring, "avail_parameters": avail_parameters}


    parameters = db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == deptno)).first()

    if parameters:
        avail_parameters = True
        parameters_vstring = parameters.vstring

    return generate_output()