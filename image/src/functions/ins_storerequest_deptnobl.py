from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Parameters

def ins_storerequest_deptnobl(dept:int, deptno:int, deptname:str):
    flag = 0
    parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, parameters


        return {"flag": flag}


    parameters = db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == deptno)).first()

    if parameters:
        deptname = parameters.vstring
        flag = 1
    else:
        deptno = dept
        flag = 2

    return generate_output()