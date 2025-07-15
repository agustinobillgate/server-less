#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_journal

def read_h_journalbl(case_type:int, billno:int, artno:int, dept:int, datum:date, waehrungno:int):
    t_h_journal_data = []
    h_journal = None

    t_h_journal = None

    t_h_journal_data, T_h_journal = create_model_like(H_journal)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_journal_data, h_journal
        nonlocal case_type, billno, artno, dept, datum, waehrungno


        nonlocal t_h_journal
        nonlocal t_h_journal_data

        return {"t-h-journal": t_h_journal_data}

    if not CONNECTED ("vhp"):

        return generate_output()

    if case_type == 1:

        for h_journal in db_session.query(H_journal).filter(
                 (H_journal.rechnr == billno) & (H_journal.departement == dept) & (H_journal.bill_datum == datum)).order_by(H_journal.sysdate, H_journal.zeit).all():
            t_h_journal = T_h_journal()
            t_h_journal_data.append(t_h_journal)

            buffer_copy(h_journal, t_h_journal)

    elif case_type == 2:

        for h_journal in db_session.query(H_journal).filter(
                 (H_journal.rechnr == billno) & (H_journal.departement == dept) & (H_journal.bill_datum == datum) & (H_journal.waehrungsnr == waehrungno)).order_by(H_journal._recid).all():
            t_h_journal = T_h_journal()
            t_h_journal_data.append(t_h_journal)

            buffer_copy(h_journal, t_h_journal)


    return generate_output()