#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_journal, Bill_line

def ar_subledger_prepare_disp_restbillbl(s_recid:int):

    prepare_cache ([Bill_line])

    billno = 0
    t_h_journal_list = []
    i:int = 0
    h_journal = bill_line = None

    t_h_journal = bline = None

    t_h_journal_list, T_h_journal = create_model_like(H_journal)

    Bline = create_buffer("Bline",Bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billno, t_h_journal_list, i, h_journal, bill_line
        nonlocal s_recid
        nonlocal bline


        nonlocal t_h_journal, bline
        nonlocal t_h_journal_list

        return {"billno": billno, "t-h-journal": t_h_journal_list}

    bline = get_cache (Bill_line, {"_recid": [(eq, s_recid)]})
    for i in range(1,length(bline.bezeich)  + 1) :

        if substring(bline.bezeich, i - 1, 1) == ("*").lower() :
            billno = to_int(substring(bline.bezeich, i + 1 - 1, length(bline.bezeich)))
            i = 999

    for h_journal in db_session.query(H_journal).filter(
             (H_journal.rechnr == billno) & (H_journal.departement == bline.departement) & (H_journal.bill_datum == bline.bill_datum)).order_by(H_journal._recid).all():
        t_h_journal = T_h_journal()
        t_h_journal_list.append(t_h_journal)

        buffer_copy(h_journal, t_h_journal)

    return generate_output()