from functions.additional_functions import *
import decimal
from models import L_order

def chg_pr_def_actionbl(s_recid:int, bez:str):
    l_order = None

    l_od = None

    L_od = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order
        nonlocal l_od


        nonlocal l_od
        return {}


    l_od = db_session.query(L_od).filter(
            (L_od._recid == s_recid)).first()
    l_od.quality = to_string(substring(l_od.quality, 0, 11) , "x(11)") + bez

    l_od = db_session.query(L_od).first()

    return generate_output()