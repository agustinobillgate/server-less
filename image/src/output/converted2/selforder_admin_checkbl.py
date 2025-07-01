#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener

def selforder_admin_checkbl(deptno:int, grup:int, paramnr:int, intval:int, decval:Decimal, dateval:date, logval:bool, charval:string):
    err_flag = False
    bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, bediener
        nonlocal deptno, grup, paramnr, intval, decval, dateval, logval, charval

        return {"err_flag": err_flag}


    if paramnr == 9 and grup == 1 and charval != "":

        bediener = get_cache (Bediener, {"userinit": [(eq, charval)]})

        if not bediener:
            err_flag = True

    return generate_output()