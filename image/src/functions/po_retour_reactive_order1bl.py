from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_order

def po_retour_reactive_order1bl(case_type:int, docu_nr:str):
    avail_l_od = False
    l_order = None

    l_od = None

    L_od = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_od, l_order
        nonlocal l_od


        nonlocal l_od
        return {"avail_l_od": avail_l_od}


    if case_type == 1:

        l_od = db_session.query(L_od).filter(
                (func.lower(L_od.(docu_nr).lower()) == (docu_nr).lower()) &  (L_od.pos > 0) &  ((L_od.anzahl > L_od.geliefert))).first()

        if l_od:
            avail_l_od = True

    elif case_type == 2:

        for l_od in db_session.query(L_od).filter(
                (func.lower(L_od.(docu_nr).lower()) == (docu_nr).lower()) &  (L_od.pos >= 0) &  (L_od.loeschflag == 1)).all():
            l_od.loeschflag = 0


    return generate_output()