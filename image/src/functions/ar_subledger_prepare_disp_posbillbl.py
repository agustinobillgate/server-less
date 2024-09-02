from functions.additional_functions import *
import decimal
from models import H_journal, Debitor

def ar_subledger_prepare_disp_posbillbl(a_rechnr:int, a_dept:int, a_rid:int):
    t_h_journal_list = []
    h_journal = debitor = None

    t_h_journal = ar_buff = None

    t_h_journal_list, T_h_journal = create_model_like(H_journal)

    Ar_buff = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_journal_list, h_journal, debitor
        nonlocal ar_buff


        nonlocal t_h_journal, ar_buff
        nonlocal t_h_journal_list
        return {"t-h-journal": t_h_journal_list}

    ar_buff = db_session.query(Ar_buff).filter(
            (Ar_buff._recid == a_rid)).first()

    for h_journal in db_session.query(H_journal).filter(
            (H_journal.bill_datum == ar_buff.rgdatum) &  (H_journal.rechnr == a_rechnr) &  (H_journal.departement == a_dept)).all():
        t_h_journal = T_h_journal()
        t_h_journal_list.append(t_h_journal)

        buffer_copy(h_journal, t_h_journal)

    return generate_output()