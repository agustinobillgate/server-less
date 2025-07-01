#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def ins_storerequest_deptnobl(dept:int, deptno:int, deptname:string):

    prepare_cache ([Parameters])

    flag = 0
    parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, parameters
        nonlocal dept, deptno, deptname

        return {"deptno": deptno, "deptname": deptname, "flag": flag}


    parameters = db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == deptno)).first()

    if parameters:
        deptname = parameters.vstring
        flag = 1
    else:
        deptno = dept
        flag = 2

    return generate_output()