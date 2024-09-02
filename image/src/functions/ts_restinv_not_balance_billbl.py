from functions.additional_functions import *
import decimal
from models import Htparam, H_bill

def ts_restinv_not_balance_billbl(pvilanguage:int, curr_dept:int, curr_waiter:int):
    msg_str = ""
    p_852 = 0
    lvcarea:str = "TS_restinv"
    htparam = h_bill = None

    hbill = None

    Hbill = H_bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, p_852, lvcarea, htparam, h_bill
        nonlocal hbill


        nonlocal hbill
        return {"msg_str": msg_str, "p_852": p_852}

    def not_balance_bill():

        nonlocal msg_str, p_852, lvcarea, htparam, h_bill
        nonlocal hbill


        nonlocal hbill

        found:bool = False
        Hbill = H_bill

        hbill = db_session.query(Hbill).filter(
                (Hbill.departement == curr_dept) &  (Hbill.kellner_nr == curr_waiter) &  (Hbill.flag == 0)).first()

        if hbill:
            msg_str = msg_str + chr(2) + "&W" + translateExtended ("Not balanced open bill(s) found:", lvcarea, "") + chr(10) + translateExtended ("BillNo:", lvcarea, "") + " " + to_string(hbill.rechnr) + "  " + translateExtended ("TableNo:", lvcarea, "") + " " + to_string(hbill.tischnr) + chr(10) + translateExtended ("Balance", lvcarea, "") + " " + trim(to_string(hbill.saldo, "->>,>>>,>>9.99"))
            found = True

    not_balance_bill()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 852)).first()
    p_852 = htparam.finteger

    return generate_output()