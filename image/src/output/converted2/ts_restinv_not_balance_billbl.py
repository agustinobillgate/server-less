#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, H_bill

def ts_restinv_not_balance_billbl(pvilanguage:int, curr_dept:int, curr_waiter:int):

    prepare_cache ([Htparam, H_bill])

    msg_str = ""
    p_852 = 0
    lvcarea:string = "TS-restinv"
    htparam = h_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, p_852, lvcarea, htparam, h_bill
        nonlocal pvilanguage, curr_dept, curr_waiter

        return {"msg_str": msg_str, "p_852": p_852}

    def not_balance_bill():

        nonlocal msg_str, p_852, lvcarea, htparam, h_bill
        nonlocal pvilanguage, curr_dept, curr_waiter

        hbill = None
        found:bool = False
        Hbill =  create_buffer("Hbill",H_bill)

        hbill = get_cache (H_bill, {"departement": [(eq, curr_dept)],"kellner_nr": [(eq, curr_waiter)],"flag": [(eq, 0)]})

        if hbill:
            msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Not balanced open bill(s) found:", lvcarea, "") + chr_unicode(10) + translateExtended ("BillNo:", lvcarea, "") + " " + to_string(hbill.rechnr) + " " + translateExtended ("TableNo:", lvcarea, "") + " " + to_string(hbill.tischnr) + chr_unicode(10) + translateExtended ("Balance", lvcarea, "") + " " + trim(to_string(hbill.saldo, "->>,>>>,>>9.99"))
            found = True


    not_balance_bill()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 852)]})
    p_852 = htparam.finteger

    return generate_output()