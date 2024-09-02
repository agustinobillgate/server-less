from functions.additional_functions import *
import decimal
from datetime import date
from models import H_bill, H_artikel, Queasy

def ts_restinv_run_helpbl(kpr_time:int, kpr_recid:int, bill_date:date, tischnr:int, curr_dept:int, amount:decimal):
    fl_code = 0
    t_h_artikel1_list = []
    t_h_bill_list = []
    h_bill = h_artikel = queasy = None

    t_h_bill = t_h_artikel1 = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_h_artikel1_list, T_h_artikel1 = create_model_like(H_artikel, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, t_h_artikel1_list, t_h_bill_list, h_bill, h_artikel, queasy


        nonlocal t_h_bill, t_h_artikel1
        nonlocal t_h_bill_list, t_h_artikel1_list
        return {"fl_code": fl_code, "t-h-artikel1": t_h_artikel1_list, "t-h-bill": t_h_bill_list}


    if (kpr_time - get_current_time_in_seconds()) >= 300:
        kpr_time = get_current_time_in_seconds()

    if kpr_recid == 0:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 3) &  (Queasy.number1 != 0) &  ((Queasy.char1 != "") |  (Queasy.char3 != "")) &  ((Queasy.date1 == bill_date))).first()

        if queasy:
            kpr_recid = to_int(queasy._recid)


        kpr_time = get_current_time_in_seconds()

    elif kpr_recid != 0 and (get_current_time_in_seconds() > (kpr_time + 30)):

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == kpr_recid)).first()

        if queasy and queasy.number1 != 0:
            fl_code = 1
        kpr_recid = 0
        kpr_time = get_current_time_in_seconds()

    h_bill = db_session.query(H_bill).filter(
            (H_bill.tischnr == tischnr) &  (H_bill.departement == curr_dept) &  (H_bill.flag == 0)).first()

    if h_bill:
        t_h_bill = T_h_bill()
        t_h_bill_list.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    for h_artikel in db_session.query(H_artikel).filter(
            (H_artikel.departement == curr_dept)).all():
        t_h_artikel1 = T_h_artikel1()
        t_h_artikel1_list.append(t_h_artikel1)

        buffer_copy(h_artikel, t_h_artikel1)
        t_h_artikel1.rec_id = h_artikel._recid

    return generate_output()