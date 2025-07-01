#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line

def setup_room_reslinebl(zinr:string):
    err_flag = 0
    res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, res_line
        nonlocal zinr

        return {"err_flag": err_flag}


    res_line = get_cache (Res_line, {"zinr": [(eq, zinr)],"resstatus": [(ne, 8),(ne, 9),(ne, 12),(ne, 99)]})

    if res_line:
        err_flag = 1

    return generate_output()