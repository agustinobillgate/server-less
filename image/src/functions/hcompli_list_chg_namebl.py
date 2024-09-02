from functions.additional_functions import *
import decimal
from datetime import date
from models import H_bill, H_journal

def hcompli_list_chg_namebl(c_list_rechnr:int, c_list_dept:int, guestname:str, c_list_datum:date, c_list_p_artnr:int):
    h_bill = h_journal = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill, h_journal


        return {}


    h_bill = db_session.query(H_bill).filter(
            (H_bill.rechnr == c_list_rechnr) &  (H_bill.departement == c_list_dept)).first()

    if h_bill:

        h_bill = db_session.query(H_bill).first()
        h_bill.bilname = guestname

        h_bill = db_session.query(H_bill).first()

    h_journal = db_session.query(H_journal).filter(
            (H_journal.bill_datum == c_list_datum) &  (H_journal.departement == c_list_dept) &  (H_journal.segmentcode == c_list_p_artnr) &  (H_journal.rechnr == c_list_rechnr) &  (H_journal.zeit >= 0)).first()
    while None != h_journal:

        h_journal = db_session.query(H_journal).first()
        h_journal.aendertext = guestname

        h_journal = db_session.query(H_journal).first()

        h_journal = db_session.query(H_journal).filter(
                (H_journal.bill_datum == c_list_datum) &  (H_journal.departement == c_list_dept) &  (H_journal.segmentcode == c_list_p_artnr) &  (H_journal.rechnr == c_list_rechnr) &  (H_journal.zeit >= 0)).first()

    return generate_output()