#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_op

def po_stockin_mi_allbl(lscheinnr:string, docu_nr:string):
    fl_code = 0
    l_op = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, l_op
        nonlocal lscheinnr, docu_nr

        return {"fl_code": fl_code}


    l_op = get_cache (L_op, {"op_art": [(eq, 1)],"loeschflag": [(le, 1)],"lscheinnr": [(eq, lscheinnr)],"docu_nr": [(ne, docu_nr)]})

    if l_op:
        fl_code = 1

        return generate_output()

    return generate_output()