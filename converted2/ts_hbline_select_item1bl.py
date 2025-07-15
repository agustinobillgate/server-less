#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_journal

def ts_hbline_select_item1bl(billdate:date, dept:int, curr_rechnr:int):

    prepare_cache ([H_journal])

    voucher = ""
    h_journal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal voucher, h_journal
        nonlocal billdate, dept, curr_rechnr

        return {"voucher": voucher}


    h_journal = db_session.query(H_journal).filter(
             (H_journal.bill_datum == billdate) & (H_journal.departement == dept) & (H_journal.rechnr == curr_rechnr) & (H_journal.wabkurz != "")).order_by(H_journal._recid.desc()).first()

    if h_journal:
        voucher = h_journal.wabkurz

    return generate_output()