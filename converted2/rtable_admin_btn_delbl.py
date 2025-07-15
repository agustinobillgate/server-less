#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Tisch, H_bill

def rtable_admin_btn_delbl(dept:int, t_tischnr:int):
    flag = 0
    tisch = h_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, tisch, h_bill
        nonlocal dept, t_tischnr

        return {"flag": flag}


    tisch = get_cache (Tisch, {"departement": [(eq, dept)],"tischnr": [(eq, t_tischnr)]})

    h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"tischnr": [(eq, t_tischnr)]})

    if h_bill:
        flag = 1
    else:
        pass
        db_session.delete(tisch)

    return generate_output()