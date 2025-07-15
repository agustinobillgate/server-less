#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt

def prepare_kitchen_displaybl(deptno:int):

    prepare_cache ([Hoteldpt])

    deptname = ""
    hoteldpt = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal deptname, hoteldpt
        nonlocal deptno

        return {"deptname": deptname}


    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, deptno)]})

    if hoteldpt:
        deptname = hoteldpt.depart.upper()

    return generate_output()