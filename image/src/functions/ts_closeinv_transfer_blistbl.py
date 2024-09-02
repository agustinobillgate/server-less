from functions.additional_functions import *
import decimal
from datetime import date
from models import H_bill_line

def ts_closeinv_transfer_blistbl(b_list_rechnr:int, curr_dept:int, b_list_artnr:int, b_list_sysdate:date, b_list_zeit:int):
    avail_h_bill_line = False
    h_bill_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_h_bill_line, h_bill_line


        return {"avail_h_bill_line": avail_h_bill_line}


    h_bill_line = db_session.query(H_bill_line).filter(
            (H_bill_line.rechnr == b_list_rechnr) &  (H_bill_line.departement == curr_dept) &  (H_bill_line.artnr == b_list_artnr) &  (H_bill_line.sysdate == b_list_sysdate) &  (H_bill_line.zeit == b_list_zeit)).first()

    if h_bill_line:
        avail_h_bill_line = True

    return generate_output()