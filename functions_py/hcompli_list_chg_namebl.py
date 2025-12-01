#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill, H_journal

def hcompli_list_chg_namebl(c_list_rechnr:int, c_list_dept:int, guestname:string, c_list_datum:date, c_list_p_artnr:int):

    prepare_cache ([H_bill])

    h_bill = h_journal = None

    db_session = local_storage.db_session
    guestname = guestname.strip()

    def generate_output():
        nonlocal h_bill, h_journal
        nonlocal c_list_rechnr, c_list_dept, guestname, c_list_datum, c_list_p_artnr

        return {}


    # h_bill = get_cache (H_bill, {"rechnr": [(eq, c_list_rechnr)],"departement": [(eq, c_list_dept)]})
    h_bill = db_session.query(H_bill).filter(
                 (H_bill.rechnr == c_list_rechnr) & (H_bill.departement == c_list_dept)).with_for_update().first()

    if h_bill:
        h_bill.bilname = guestname

    # h_journal = get_cache (H_journal, {"bill_datum": [(eq, c_list_datum)],"departement": [(eq, c_list_dept)],
    # "segmentcode": [(eq, c_list_p_artnr)],"rechnr": [(eq, c_list_rechnr)],"zeit": [(ge, 0)]})
    h_journal = db_session.query(H_journal).filter(
                 (H_journal.bill_datum == c_list_datum) & (H_journal.departement == c_list_dept) & 
                 (H_journal.segmentcode == c_list_p_artnr) & (H_journal.rechnr == c_list_rechnr) & (H_journal.zeit >= 0)).with_for_update().first()
    while None != h_journal:
        h_journal.aendertext = guestname

        curr_recid = h_journal._recid
        h_journal = db_session.query(H_journal).filter(
                 (H_journal.bill_datum == c_list_datum) & (H_journal.departement == c_list_dept) & 
                 (H_journal.segmentcode == c_list_p_artnr) & (H_journal.rechnr == c_list_rechnr) & (H_journal.zeit >= 0) & (H_journal._recid > curr_recid)).with_for_update().first()

    return generate_output()