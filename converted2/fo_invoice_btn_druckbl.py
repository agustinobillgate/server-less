#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_journal, H_bill_line, H_bill

def fo_invoice_btn_druckbl(recid_hjournal:int, recid_hbill_line:int):

    prepare_cache ([H_journal, H_bill_line, H_bill])

    do_it = False
    recid_h_bill = 0
    h_journal = h_bill_line = h_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, recid_h_bill, h_journal, h_bill_line, h_bill
        nonlocal recid_hjournal, recid_hbill_line

        return {"do_it": do_it, "recid_h_bill": recid_h_bill}


    if recid_hjournal != 0:

        h_journal = get_cache (H_journal, {"_recid": [(eq, recid_hjournal)]})

    elif recid_hbill_line != 0:

        h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, recid_hbill_line)]})

    if h_journal:

        h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

    elif h_bill_line:

        h_bill = get_cache (H_bill, {"rechnr": [(eq, h_bill_line.rechnr)],"departement": [(eq, h_bill_line.departement)]})

    if h_bill:
        do_it = True
        recid_h_bill = h_bill._recid

    return generate_output()