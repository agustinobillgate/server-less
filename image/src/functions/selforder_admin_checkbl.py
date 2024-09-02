from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener

def selforder_admin_checkbl(deptno:int, grup:int, paramnr:int, intval:int, decval:decimal, dateval:date, logval:bool, charval:str):
    err_flag = False
    bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, bediener


        return {"err_flag": err_flag}


    if paramnr == 9 and grup == 1 and charval != "":

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (charval).lower())).first()

        if not bediener:
            err_flag = True

    return generate_output()