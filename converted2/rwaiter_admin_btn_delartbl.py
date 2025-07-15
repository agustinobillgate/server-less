#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Kellner, Kellne1

def rwaiter_admin_btn_delartbl(dept:int, r_kellner:int, r_kellne1:int, t_kellner_nr:int):
    flag = 0
    h_bill = kellner = kellne1 = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, h_bill, kellner, kellne1
        nonlocal dept, r_kellner, r_kellne1, t_kellner_nr

        return {"flag": flag}


    h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"kellner_nr": [(eq, t_kellner_nr)],"flag": [(eq, 0)]})

    if h_bill:
        flag = 1
    else:

        kellner = get_cache (Kellner, {"_recid": [(eq, r_kellner)]})

        if kellner:
            pass
            db_session.delete(kellner)

        kellne1 = get_cache (Kellne1, {"_recid": [(eq, r_kellne1)]})

        if kellne1:
            pass
            db_session.delete(kellne1)

    return generate_output()