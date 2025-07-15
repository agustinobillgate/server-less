#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_journal, Debitor

def ar_subledger_prepare_disp_posbillbl(a_rechnr:int, a_dept:int, a_rid:int):

    prepare_cache ([Debitor])

    t_h_journal_data = []
    h_journal = debitor = None

    t_h_journal = ar_buff = None

    t_h_journal_data, T_h_journal = create_model_like(H_journal)

    Ar_buff = create_buffer("Ar_buff",Debitor)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_journal_data, h_journal, debitor
        nonlocal a_rechnr, a_dept, a_rid
        nonlocal ar_buff


        nonlocal t_h_journal, ar_buff
        nonlocal t_h_journal_data

        return {"t-h-journal": t_h_journal_data}

    ar_buff = get_cache (Debitor, {"_recid": [(eq, a_rid)]})

    if ar_buff:

        for h_journal in db_session.query(H_journal).filter(
                 (H_journal.bill_datum == ar_buff.rgdatum) & (H_journal.rechnr == a_rechnr) & (H_journal.departement == a_dept)).order_by(H_journal._recid).all():
            t_h_journal = T_h_journal()
            t_h_journal_data.append(t_h_journal)

            buffer_copy(h_journal, t_h_journal)
    else:

        return generate_output()

    return generate_output()