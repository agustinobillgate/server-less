from functions.additional_functions import *
import decimal
from datetime import date
from models import H_bill, H_bill_line, Htparam

def prepare_ts_restinv_close_shiftbl(pvilanguage:int, curr_dept:int, curr_waiter:int):
    billdate = None
    msg_str = ""
    shift_list_list = []
    lvcarea:str = "TS_restinv"
    h_bill = h_bill_line = htparam = None

    shift_list = hbill = hbline = None

    shift_list_list, Shift_list = create_model("Shift_list", {"rechnr":int, "tischnr":int, "selectflag":bool, "bstr":str})

    Hbill = H_bill
    Hbline = H_bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, msg_str, shift_list_list, lvcarea, h_bill, h_bill_line, htparam
        nonlocal hbill, hbline


        nonlocal shift_list, hbill, hbline
        nonlocal shift_list_list
        return {"billdate": billdate, "msg_str": msg_str, "shift-list": shift_list_list}

    h_bill = db_session.query(H_bill).filter(
            (H_bill.departement == curr_dept) &  (H_bill.flag == 0) &  (H_bill.kellner_nr == curr_waiter)).first()

    if h_bill:
        msg_str = msg_str + chr(2) + translateExtended ("Opened bill found:", lvcarea, "") + " " + translateExtended ("Table No:", lvcarea, "") + " " + to_string(h_bill.tischnr) + chr(10) + translateExtended ("Close Shift not possible.", lvcarea, "")

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate
    shift_list_list.clear()

    hbill_obj_list = []
    for hbill, hbline in db_session.query(Hbill, Hbline).join(Hbline,(Hbline.rechnr == Hbill.rechnr) &  (Hbline.bill_datum == billdate) &  (Hbline.departement == curr_dept) &  (Hbline.zeit >= 0) &  (Hbline.betriebsnr == 0)).filter(
            (Hbill.flag == 1) &  (Hbill.departement == curr_dept) &  (Hbill.kellner_nr == curr_waiter)).all():
        if hbill._recid in hbill_obj_list:
            continue
        else:
            hbill_obj_list.append(hbill._recid)


        shift_list = Shift_list()
        shift_list_list.append(shift_list)

        shift_list.rechnr = hbill.rechnr
        shift_list.tischnr = hbill.tischnr

    return generate_output()