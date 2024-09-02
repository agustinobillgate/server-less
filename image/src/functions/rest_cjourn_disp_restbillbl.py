from functions.additional_functions import *
import decimal
from datetime import date
from models import H_journal

def rest_cjourn_disp_restbillbl(rechno:int, dept:int, billdate:date):
    hj_buff_list = []
    h_journal = None

    hj_buff = None

    hj_buff_list, Hj_buff = create_model_like(H_journal, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hj_buff_list, h_journal


        nonlocal hj_buff
        nonlocal hj_buff_list
        return {"hj-buff": hj_buff_list}

    for h_journal in db_session.query(H_journal).filter(
            (H_journal.rechnr == rechno) &  (H_journal.departement == dept) &  (H_journal.bill_datum == billdate)).all():
        hj_buff = Hj_buff()
        hj_buff_list.append(hj_buff)

        buffer_copy(h_journal, hj_buff)
        hj_buff.rec_id = h_journal._recid

    return generate_output()