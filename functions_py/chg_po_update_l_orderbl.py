#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order
from sqlalchemy.orm.attributes import flag_modified

def chg_po_update_l_orderbl(rec_id:int, potype:int, cost_acct:string, bez:string, billdate:date, bediener_username:string):

    prepare_cache ([L_order])

    l_order = None

    db_session = local_storage.db_session
    cost_acct = cost_acct.strip()
    bez = bez.strip()
    bediener_username = bediener_username.strip()

    def generate_output():
        nonlocal l_order
        nonlocal rec_id, potype, cost_acct, bez, billdate, bediener_username

        return {}


    # l_order = get_cache (L_order, {"_recid": [(eq, rec_id)]})
    l_order = db_session.query(L_order).filter(
             (L_order._recid == rec_id)).with_for_update().first()

    if potype == 2:
        l_order.stornogrund = to_string(cost_acct, "x(12)") + bez
    l_order.lieferdatum = billdate
    l_order.lief_fax[1] = bediener_username
    flag_modified(l_order, "lief_fax")

    return generate_output()