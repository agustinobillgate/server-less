#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kellner, Htparam, Hoteldpt, H_journal

def prepare_ts_oldhbillbl(rechnr:int, knr:int, curr_dept:int, income_audit:bool):

    prepare_cache ([Htparam, H_journal])

    supervise = False
    bill_date = None
    kellner = htparam = hoteldpt = h_journal = None

    waiter = None

    Waiter = create_buffer("Waiter",Kellner)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal supervise, bill_date, kellner, htparam, hoteldpt, h_journal
        nonlocal rechnr, knr, curr_dept, income_audit
        nonlocal waiter


        nonlocal waiter

        return {"rechnr": rechnr, "supervise": supervise, "bill_date": bill_date}

    def find_billno():

        nonlocal supervise, bill_date, kellner, htparam, hoteldpt, h_journal
        nonlocal rechnr, knr, curr_dept, income_audit
        nonlocal waiter


        nonlocal waiter

        for h_journal in db_session.query(H_journal).filter(
                 (H_journal.bill_datum == bill_date) & (H_journal.departement == curr_dept) & (H_journal.kellner_nr == knr) & (H_journal.zeit > 0)).order_by(H_journal.sysdate.desc(), H_journal.zeit.desc()).all():
            rechnr = h_journal.rechnr

            return

    waiter = db_session.query(Waiter).filter(
             (Waiter.kellner_nr == knr) & (Waiter.departement == curr_dept)).first()
    supervise = (None != waiter and waiter.masterkey) or income_audit

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

    if rechnr == 0 and waiter:
        find_billno()

    return generate_output()