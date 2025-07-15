#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Htparam, Guest

def ts_rnonstay_check_creditlimitbl(rechnr:int, pvilanguage:int, rec_id:int, balance:Decimal, overcl_flag:bool):

    prepare_cache ([Bill, Htparam, Guest])

    err_flag = 0
    msg_str = ""
    lvcarea:string = "TS-rnonstay"
    bill = htparam = guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, msg_str, lvcarea, bill, htparam, guest
        nonlocal rechnr, pvilanguage, rec_id, balance, overcl_flag

        return {"err_flag": err_flag, "msg_str": msg_str}

    def check_creditlimit():

        nonlocal err_flag, msg_str, lvcarea, bill, htparam, guest
        nonlocal rechnr, pvilanguage, rec_id, balance, overcl_flag

        klimit:Decimal = to_decimal("0.0")
        answer:bool = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 68)]})

        guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

        if guest.kreditlimit != 0:
            klimit =  to_decimal(guest.kreditlimit)
        else:

            if htparam.fdecimal != 0:
                klimit =  to_decimal(htparam.fdecimal)
            else:
                klimit =  to_decimal(htparam.finteger)

        if (bill.saldo + balance) > klimit:

            if overcl_flag:
                err_flag = 1
                msg_str = msg_str + chr_unicode(2) + translateExtended ("OVER Credit Limit found !!!", lvcarea, "") + chr_unicode(10) + translateExtended ("Given Limit =", lvcarea, "") + " " + trim(to_string(klimit, ">>>,>>>,>>>,>>9")) + chr_unicode(10) + translateExtended ("Bill balance will be", lvcarea, "") + " " + trim(to_string((bill.saldo + balance) , ">>>,>>>,>>>,>>9.99")) + chr_unicode(10) + translateExtended ("Bill Transfer no longer possible.", lvcarea, "")

                return
            msg_str = msg_str + chr_unicode(2) + "&Q" + translateExtended ("OVER Credit Limit found !!!", lvcarea, "") + chr_unicode(10) + translateExtended ("Given Limit =", lvcarea, "") + " " + trim(to_string(klimit, ">>>,>>>,>>>,>>9")) + chr_unicode(10) + translateExtended ("Bill balance will be", lvcarea, "") + " " + trim(to_string((bill.saldo + balance) , ">>>,>>>,>>>,>>9.99")) + chr_unicode(10) + translateExtended ("CANCEL the Bill Transfer?", lvcarea, "")

    bill = get_cache (Bill, {"_recid": [(eq, rec_id)]})
    check_creditlimit()

    return generate_output()