from functions.additional_functions import *
import decimal
from datetime import date
from models import H_bill, Kellner, Umsatz, H_bill_line, H_journal

def waiter_transfer(k1:int, k2:int, curr_dept:int, bill_date:date):
    h_bill = kellner = umsatz = h_bill_line = h_journal = None

    hbill = kellner1 = kellner2 = umsatz2 = None

    Hbill = create_buffer("Hbill",H_bill)
    Kellner1 = create_buffer("Kellner1",Kellner)
    Kellner2 = create_buffer("Kellner2",Kellner)
    Umsatz2 = create_buffer("Umsatz2",Umsatz)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill, kellner, umsatz, h_bill_line, h_journal
        nonlocal k1, k2, curr_dept, bill_date
        nonlocal hbill, kellner1, kellner2, umsatz2


        nonlocal hbill, kellner1, kellner2, umsatz2

        return {}


    kellner1 = db_session.query(Kellner1).filter(
             (Kellner1.kellner_nr == k1) & (Kellner1.departement == curr_dept)).first()

    kellner2 = db_session.query(Kellner2).filter(
             (Kellner2.kellner_nr == k2) & (Kellner2.departement == curr_dept)).first()

    hbill = db_session.query(Hbill).filter(
             (Hbill.flag == 0) & (Hbill.departement == curr_dept) & (Hbill.kellner_nr == kellner1.kellner_nr)).first()
    while None != hbill:
        hbill.kellner_nr = k2

        h_bill_line = db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == hbill.rechnr) & (H_bill_line.departement == curr_dept)).first()

        if h_bill_line:
            h_journal = H_journal()
            db_session.add(h_journal)

            h_journal.rechnr = hbill.rechnr
            h_journal.departement = hbill.departement
            h_journal.bill_datum = h_bill_line.bill_datum
            h_journal.tischnr = hbill.tischnr
            h_journal.zeit = get_current_time_in_seconds()
            h_journal.kellner_nr = k1


            h_journal.bezeich = "Waiter Transfer To" + " " + to_string(k2)

        curr_recid = hbill._recid
        hbill = db_session.query(Hbill).filter(
                 (Hbill.flag == 0) & (Hbill.departement == curr_dept) & (Hbill.kellner_nr == kellner1.kellner_nr) & (Hbill._recid > curr_recid)).first()

    return generate_output()