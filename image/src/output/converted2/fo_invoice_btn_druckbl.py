from functions.additional_functions import *
import decimal
from models import H_journal, H_bill_line, H_bill

def fo_invoice_btn_druckbl(recid_hjournal:int, recid_hbill_line:int):
    do_it = False
    recid_h_bill = 0
    h_journal = h_bill_line = h_bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, recid_h_bill, h_journal, h_bill_line, h_bill
        nonlocal recid_hjournal, recid_hbill_line


        return {"do_it": do_it, "recid_h_bill": recid_h_bill}


    if recid_hjournal != 0:

        h_journal = db_session.query(H_journal).filter(
                 (H_journal._recid == recid_hjournal)).first()

    elif recid_hbill_line != 0:

        h_bill_line = db_session.query(H_bill_line).filter(
                 (H_bill_line._recid == recid_hbill_line)).first()

    if h_journal:

        h_bill = db_session.query(H_bill).filter(
                 (H_bill.rechnr == h_journal.rechnr) & (H_bill.departement == h_journal.departement)).first()

    elif h_bill_line:

        h_bill = db_session.query(H_bill).filter(
                 (H_bill.rechnr == h_bill_line.rechnr) & (H_bill.departement == h_bill_line.departement)).first()

    if h_bill:
        do_it = True
        recid_h_bill = h_bill._recid

    return generate_output()