from functions.additional_functions import *
import decimal
from models import H_journal, Blinehis

def ar_subledger_prepare_disp1_restbillbl(s_recid:int):
    billno = 0
    t_h_journal_list = []
    i:int = 0
    h_journal = blinehis = None

    t_h_journal = bline = None

    t_h_journal_list, T_h_journal = create_model_like(H_journal)

    Bline = Blinehis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billno, t_h_journal_list, i, h_journal, blinehis
        nonlocal bline


        nonlocal t_h_journal, bline
        nonlocal t_h_journal_list
        return {"billno": billno, "t-h-journal": t_h_journal_list}

    bline = db_session.query(Bline).filter(
            (Bline._recid == s_recid)).first()
    for i in range(1,len(bline.bezeich)  + 1) :

        if substring(bline.bezeich, i - 1, 1) == "*":
            billno = to_int(substring(bline.bezeich, i + 1 - 1, len(bline.bezeich)))
            i = 999

    for h_journal in db_session.query(H_journal).filter(
            (H_journal.rechnr == billno) &  (H_journal.departement == bline.departement) &  (H_journal.bill_datum == bline.bill_datum)).all():
        t_h_journal = T_h_journal()
        t_h_journal_list.append(t_h_journal)

        buffer_copy(h_journal, t_h_journal)

    return generate_output()