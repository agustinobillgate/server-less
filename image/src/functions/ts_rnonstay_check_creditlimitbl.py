from functions.additional_functions import *
import decimal
from models import Bill, Htparam, Guest

def ts_rnonstay_check_creditlimitbl(rechnr:int, pvilanguage:int, rec_id:int, balance:decimal, overcl_flag:bool):
    err_flag = 0
    msg_str = ""
    lvcarea:str = "TS_rnonstay"
    bill = htparam = guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, msg_str, lvcarea, bill, htparam, guest


        return {"err_flag": err_flag, "msg_str": msg_str}

    def check_creditlimit():

        nonlocal err_flag, msg_str, lvcarea, bill, htparam, guest

        klimit:decimal = 0
        answer:bool = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 68)).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == bill.gastnr)).first()

        if guest.kreditlimit != 0:
            klimit = guest.kreditlimit
        else:

            if htparam.fdecimal != 0:
                klimit = htparam.fdecimal
            else:
                klimit = htparam.finteger

        if (bill.saldo + balance) > klimit:

            if overcl_flag:
                err_flag = 1
                msg_str = msg_str + chr(2) + translateExtended ("OVER Credit Limit found !!!", lvcarea, "") + chr(10) + translateExtended ("Given Limit   == ", lvcarea, "") + " " + trim(to_string(klimit, ">>>,>>>,>>>,>>9")) + chr(10) + translateExtended ("Bill balance will be", lvcarea, "") + " " + trim(to_string((bill.saldo + balance) , ">>>,>>>,>>>,>>9.99")) + chr(10) + translateExtended ("Bill Transfer no longer possible.", lvcarea, "")

                return
            msg_str = msg_str + chr(2) + "&Q" + translateExtended ("OVER Credit Limit found !!!", lvcarea, "") + chr(10) + translateExtended ("Given Limit   == ", lvcarea, "") + " " + trim(to_string(klimit, ">>>,>>>,>>>,>>9")) + chr(10) + translateExtended ("Bill balance will be", lvcarea, "") + " " + trim(to_string((bill.saldo + balance) , ">>>,>>>,>>>,>>9.99")) + chr(10) + translateExtended ("CANCEL the Bill Transfer?", lvcarea, "")


    bill = db_session.query(Bill).filter(
            (Bill._recid == rec_id)).first()
    check_creditlimit()

    return generate_output()