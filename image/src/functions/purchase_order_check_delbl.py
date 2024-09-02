from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_order

def purchase_order_check_delbl(q2_list_docu_nr:str):
    err_code = 0
    found:bool = False
    l_order = None

    l_order1 = None

    L_order1 = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, found, l_order
        nonlocal l_order1


        nonlocal l_order1
        return {"err_code": err_code}


    l_order1 = db_session.query(L_order1).filter(
                (func.lower(L_order1.docu_nr) == (q2_list_docu_nr).lower()) &  (L_order1.pos > 0) &  (L_order1.loeschflag == 0) &  ((L_order1.anzahl != L_order1.geliefert))).first()

    if l_order1:
        found = True
    else:
        while (not found) and l_order1:

            l_order1 = db_session.query(L_order1).filter(
                        (func.lower(L_order1.docu_nr) == (q2_list_docu_nr).lower()) &  (L_order1.pos > 0) &  (L_order1.loeschflag == 0) &  ((L_order1.anzahl != L_order1.geliefert))).first()

            if l_order1:
                found = True

    if not found:
        err_code = 1
    else:
        err_code = 2

    return generate_output()