#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_journal

def mbar_report_disp_restbillbl(billno:int, dept:int, datum:date):
    t_h_journal_list = []
    h_journal = None

    t_h_journal = None

    t_h_journal_list, T_h_journal = create_model_like(H_journal)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_journal_list, h_journal
        nonlocal billno, dept, datum


        nonlocal t_h_journal
        nonlocal t_h_journal_list

        return {"t-h-journal": t_h_journal_list}

    for h_journal in db_session.query(H_journal).filter(
             (H_journal.rechnr == billno) & (H_journal.departement == dept) & (H_journal.bill_datum == datum)).order_by(H_journal.sysdate, H_journal.zeit).all():
        t_h_journal = T_h_journal()
        t_h_journal_list.append(t_h_journal)

        buffer_copy(h_journal, t_h_journal)

    return generate_output()