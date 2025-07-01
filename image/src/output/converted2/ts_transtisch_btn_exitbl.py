#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Tisch, Kellner

def ts_transtisch_btn_exitbl(pvilanguage:int, tableno:int, curr_dept:int):

    prepare_cache ([Kellner])

    err_code = 0
    msg_str = ""
    t_h_bill_list = []
    lvcarea:string = "TS-transtisch"
    h_bill = tisch = kellner = None

    t_h_bill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, msg_str, t_h_bill_list, lvcarea, h_bill, tisch, kellner
        nonlocal pvilanguage, tableno, curr_dept


        nonlocal t_h_bill
        nonlocal t_h_bill_list

        return {"err_code": err_code, "msg_str": msg_str, "t-h-bill": t_h_bill_list}

    tisch = get_cache (Tisch, {"tischnr": [(eq, tableno)],"departement": [(eq, curr_dept)]})

    if not tisch:
        err_code = 1

        return generate_output()
    else:

        h_bill = get_cache (H_bill, {"tischnr": [(eq, tableno)],"departement": [(eq, curr_dept)],"flag": [(eq, 0)]})

        if h_bill:
            t_h_bill = T_h_bill()
            t_h_bill_list.append(t_h_bill)

            buffer_copy(h_bill, t_h_bill)
            t_h_bill.rec_id = h_bill._recid

            kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, curr_dept)]})

            if kellner:
                msg_str = msg_str + chr_unicode(2) + "&Q" + translateExtended ("Transfer to table served by other waiter", lvcarea, "") + chr_unicode(10) + to_string(kellner.kellner_nr) + " - " + kellner.kellnername + "?"

    return generate_output()