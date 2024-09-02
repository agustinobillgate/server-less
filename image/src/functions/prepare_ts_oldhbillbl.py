from functions.additional_functions import *
import decimal
from datetime import date
from models import Kellner, Htparam, Hoteldpt, H_journal

def prepare_ts_oldhbillbl(rechnr:int, knr:int, curr_dept:int, income_audit:bool):
    supervise = False
    bill_date = None
    kellner = htparam = hoteldpt = h_journal = None

    waiter = None

    Waiter = Kellner

    db_session = local_storage.db_session

    def generate_output():
        nonlocal supervise, bill_date, kellner, htparam, hoteldpt, h_journal
        nonlocal waiter


        nonlocal waiter
        return {"supervise": supervise, "bill_date": bill_date}

    def find_billno():

        nonlocal supervise, bill_date, kellner, htparam, hoteldpt, h_journal
        nonlocal waiter


        nonlocal waiter

        for h_journal in db_session.query(H_journal).filter(
                (H_journal.bill_datum == bill_date) &  (H_journal.departement == curr_dept) &  (H_journal.kellner_nr == knr) &  (H_journal.zeit > 0)).all():
            rechnr = h_journal.rechnr

            return


    waiter = db_session.query(Waiter).filter(
            (Waiter.kellner_nr == knr) &  (Waiter.departement == curr_dept)).first()
    supervise = (None != waiter and waiter.masterkey) or income_audit

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == curr_dept)).first()

    if rechnr == 0 and waiter:
        find_billno()

    return generate_output()