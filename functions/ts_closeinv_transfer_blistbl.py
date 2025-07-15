#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill_line

def ts_closeinv_transfer_blistbl(b_list_rechnr:int, curr_dept:int, b_list_artnr:int, b_list_sysdate:date, b_list_zeit:int):
    avail_h_bill_line = False
    h_bill_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_h_bill_line, h_bill_line
        nonlocal b_list_rechnr, curr_dept, b_list_artnr, b_list_sysdate, b_list_zeit

        return {"avail_h_bill_line": avail_h_bill_line}


    h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, b_list_rechnr)],"departement": [(eq, curr_dept)],"artnr": [(eq, b_list_artnr)],"sysdate": [(eq, b_list_sysdate)],"zeit": [(eq, b_list_zeit)]})

    if h_bill_line:
        avail_h_bill_line = True

    return generate_output()