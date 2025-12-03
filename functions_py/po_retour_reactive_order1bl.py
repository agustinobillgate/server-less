#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import L_order

def po_retour_reactive_order1bl(case_type:int, docu_nr:string):

    prepare_cache ([L_order])

    avail_l_od = False
    l_order = None

    l_od = None

    L_od = create_buffer("L_od",L_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_od, l_order
        nonlocal case_type, docu_nr
        nonlocal l_od


        nonlocal l_od

        return {"avail_l_od": avail_l_od}


    if case_type == 1:

        l_od = get_cache (L_order, {"docu_nr": [(eq, docu_nr)],"pos": [(gt, 0)],"anzahl": [(gt, L_od.geliefert)]})

        if l_od:
            avail_l_od = True

    elif case_type == 2:

        for l_od in db_session.query(L_od).filter(
                 (L_od.docu_nr == (docu_nr).lower()) & (L_od.pos >= 0) & (L_od.loeschflag == 1)).with_for_update().order_by(L_od._recid).all():
            l_od.loeschflag = 0

    return generate_output()