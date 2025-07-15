#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, H_artikel, H_bill_line

def pos_dashboard_active_billbl(post_tischnr:int, post_curr_dept:int):

    prepare_cache ([H_bill])

    actv_flag = False
    pay_flag:bool = False
    h_bill = h_artikel = h_bill_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal actv_flag, pay_flag, h_bill, h_artikel, h_bill_line
        nonlocal post_tischnr, post_curr_dept

        return {"actv_flag": actv_flag}


    h_bill = get_cache (H_bill, {"tischnr": [(eq, post_tischnr)],"departement": [(eq, post_curr_dept)],"flag": [(eq, 0)],"saldo": [(eq, 0)]})

    if h_bill:

        h_bill_line_obj_list = {}
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart != 0)).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement)).order_by(H_bill_line._recid).yield_per(100):
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True


            pay_flag = True
            break

        if pay_flag:
            actv_flag = True

    return generate_output()