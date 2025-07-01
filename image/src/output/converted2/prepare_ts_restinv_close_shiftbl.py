#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill, H_bill_line, Htparam

def prepare_ts_restinv_close_shiftbl(pvilanguage:int, curr_dept:int, curr_waiter:int):

    prepare_cache ([H_bill, Htparam])

    billdate = None
    msg_str = ""
    shift_list_list = []
    lvcarea:string = "TS-restinv"
    h_bill = h_bill_line = htparam = None

    shift_list = hbill = hbline = None

    shift_list_list, Shift_list = create_model("Shift_list", {"rechnr":int, "tischnr":int, "selectflag":bool, "bstr":string})

    Hbill = create_buffer("Hbill",H_bill)
    Hbline = create_buffer("Hbline",H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, msg_str, shift_list_list, lvcarea, h_bill, h_bill_line, htparam
        nonlocal pvilanguage, curr_dept, curr_waiter
        nonlocal hbill, hbline


        nonlocal shift_list, hbill, hbline
        nonlocal shift_list_list

        return {"billdate": billdate, "msg_str": msg_str, "shift-list": shift_list_list}

    h_bill = get_cache (H_bill, {"departement": [(eq, curr_dept)],"flag": [(eq, 0)],"kellner_nr": [(eq, curr_waiter)]})

    if h_bill:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Opened bill found:", lvcarea, "") + " " + translateExtended ("Table No:", lvcarea, "") + " " + to_string(h_bill.tischnr) + chr_unicode(10) + translateExtended ("Close Shift not possible.", lvcarea, "")

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate
    shift_list_list.clear()

    hbill_obj_list = {}
    for hbill, hbline in db_session.query(Hbill, Hbline).join(Hbline,(Hbline.rechnr == Hbill.rechnr) & (Hbline.bill_datum == billdate) & (Hbline.departement == curr_dept) & (Hbline.zeit >= 0) & (Hbline.betriebsnr == 0)).filter(
             (Hbill.flag == 1) & (Hbill.departement == curr_dept) & (Hbill.kellner_nr == curr_waiter)).order_by(Hbill.tischnr).all():
        if hbill_obj_list.get(hbill._recid):
            continue
        else:
            hbill_obj_list[hbill._recid] = True


        shift_list = Shift_list()
        shift_list_list.append(shift_list)

        shift_list.rechnr = hbill.rechnr
        shift_list.tischnr = hbill.tischnr

    return generate_output()