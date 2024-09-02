from functions.additional_functions import *
import decimal
from models import H_bill, Tisch, Kellner

def ts_transtisch_btn_exitbl(pvilanguage:int, tableno:int, curr_dept:int):
    err_code = 0
    msg_str = ""
    t_h_bill_list = []
    lvcarea:str = "TS_transtisch"
    h_bill = tisch = kellner = None

    t_h_bill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, msg_str, t_h_bill_list, lvcarea, h_bill, tisch, kellner


        nonlocal t_h_bill
        nonlocal t_h_bill_list
        return {"err_code": err_code, "msg_str": msg_str, "t-h-bill": t_h_bill_list}

    tisch = db_session.query(Tisch).filter(
            (Tischnr == tableno) &  (Tisch.departement == curr_dept)).first()

    if not tisch:
        err_code = 1

        return generate_output()
    else:

        h_bill = db_session.query(H_bill).filter(
                (H_bill.tischnr == tableno) &  (H_bill.departement == curr_dept) &  (H_bill.flag == 0)).first()

        if h_bill:
            t_h_bill = T_h_bill()
            t_h_bill_list.append(t_h_bill)

            buffer_copy(h_bill, t_h_bill)
            t_h_bill.rec_id = h_bill._recid

            kellner = db_session.query(Kellner).filter(
                    (Kellner_nr == h_bill.kellner_nr) &  (Kellner.departement == curr_dept)).first()

            if kellner:
                msg_str = msg_str + chr(2) + "&Q" + translateExtended ("Transfer to table served by other waiter", lvcarea, "") + chr(10) + to_string(kellner_nr) + " - " + kellnername + "?"
        else:

    return generate_output()