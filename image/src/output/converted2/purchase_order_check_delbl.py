#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_order

def purchase_order_check_delbl(q2_list_docu_nr:string):

    prepare_cache ([L_order])

    err_code = 0
    found:bool = False
    l_order = None

    l_order1 = None

    L_order1 = create_buffer("L_order1",L_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, found, l_order
        nonlocal q2_list_docu_nr
        nonlocal l_order1


        nonlocal l_order1

        return {"err_code": err_code}


    l_order1 = get_cache (L_order, {"docu_nr": [(eq, q2_list_docu_nr)],"pos": [(gt, 0)],"loeschflag": [(eq, 0)],"anzahl": [(ne, L_order1.geliefert)]})

    if l_order1:
        found = True
    else:
        while (not found) and l_order1:

            curr_recid = l_order1._recid
            l_order1 = db_session.query(L_order1).filter(
                         (L_order1.docu_nr == (q2_list_docu_nr).lower()) & (L_order1.pos > 0) & (L_order1.loeschflag == 0) & ((L_order1.anzahl != L_order1.geliefert)) & (L_order1._recid > curr_recid)).first()

            if l_order1:
                found = True

    if not found:
        err_code = 1
    else:
        err_code = 2

    return generate_output()