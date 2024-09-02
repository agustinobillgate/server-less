from functions.additional_functions import *
import decimal
from models import L_order

def mk_pr_defaction_b1bl(rec_id:int, bez:str):
    l_order = None

    l_od = None

    L_od = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order
        nonlocal l_od


        nonlocal l_od
        return {}


    l_order = db_session.query(L_order).filter(
            (L_order._recid == rec_id)).first()

    l_od = db_session.query(L_od).filter(
            (L_od._recid == l_order._recid)).first()
    l_od.quality = substring(l_od.quality, 0, 11) + bez

    l_od = db_session.query(L_od).first()

    return generate_output()