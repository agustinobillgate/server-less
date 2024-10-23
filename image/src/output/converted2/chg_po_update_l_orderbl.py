from functions.additional_functions import *
import decimal
from datetime import date
from models import L_order

def chg_po_update_l_orderbl(rec_id:int, potype:int, cost_acct:str, bez:str, billdate:date, bediener_username:str):
    l_order = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order
        nonlocal rec_id, potype, cost_acct, bez, billdate, bediener_username


        return {}


    l_order = db_session.query(L_order).filter(
             (L_order._recid == rec_id)).first()

    if potype == 2:
        l_order.stornogrund = to_string(cost_acct, "x(12)") + bez
    l_order.lieferdatum = billdate
    l_order.lief_fax[1] = bediener_username

    return generate_output()