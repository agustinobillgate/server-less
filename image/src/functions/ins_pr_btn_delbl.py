from functions.additional_functions import *
import decimal
from models import L_order

def ins_pr_btn_delbl(t_recid:int):
    l_order = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order


        return {}


    l_order = db_session.query(L_order).filter(
            (L_order._recid == t_recid)).first()

    l_order = db_session.query(L_order).first()
    db_session.delete(l_order)

    return generate_output()