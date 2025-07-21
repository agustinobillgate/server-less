#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 21/7/2025
# gitlab: 996
# add if available
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bill, Htparam, Guest, Res_line, Zimmer

def ts_rzinr_btn_exitbl(pvilanguage:int, fl_code:int, code:string, resnr:int, reslinnr:int, balance:Decimal):

    prepare_cache ([Queasy, Bill, Htparam, Guest, Res_line])

    bilrecid = 0
    msg_str = ""
    msg_str1 = ""
    msg_str2 = ""
    lvcarea:string = "TS-rzinr"
    queasy = bill = htparam = guest = res_line = zimmer = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bilrecid, msg_str, msg_str1, msg_str2, lvcarea, queasy, bill, htparam, guest, res_line, zimmer
        nonlocal pvilanguage, fl_code, code, resnr, reslinnr, balance

        return {"bilrecid": bilrecid, "msg_str": msg_str, "msg_str1": msg_str1, "msg_str2": msg_str2}

    def check_creditlimit():

        nonlocal bilrecid, msg_str, msg_str1, msg_str2, lvcarea, queasy, bill, htparam, guest, res_line, zimmer
        nonlocal pvilanguage, fl_code, code, resnr, reslinnr, balance

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
            msg_str1 = msg_str1 + chr_unicode(2) + "&Q" + translateExtended ("OVER Credit Limit found: ", lvcarea, "") + translateExtended ("Given Limit =", lvcarea, "") + " " + trim(to_string(klimit, ">>>,>>>,>>>,>>9")) + " / " + translateExtended ("Bill balance =", lvcarea, "") + " " + trim(to_string(bill.saldo, "->>>,>>>,>>>,>>9.99")) + chr_unicode(10) + translateExtended ("Restaurant balance =", lvcarea, "") + " " + trim(to_string(balance, "->>>,>>>,>>>,>>9.99")) + chr_unicode(10) + translateExtended ("Do you wish to CANCEL the room transfer?", lvcarea, "")


    def check_discrepancy():

        nonlocal bilrecid, msg_str, msg_str1, msg_str2, lvcarea, queasy, bill, htparam, guest, res_line, zimmer
        nonlocal pvilanguage, fl_code, code, resnr, reslinnr, balance

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if res_line:

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)],"house_status": [(ne, 0)]})

            if zimmer:
                msg_str2 = translateExtended ("Room discrepancy is found. Transaction not possible.", lvcarea, "") + chr_unicode(10) + translateExtended ("Please contact Front Office.", lvcarea, "")

    if fl_code == 1:

        queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(code))]})

        if queasy and queasy.logi1:
            msg_str = msg_str + chr_unicode(2) + "&Q" + translateExtended ("CASH BASIS Billing Instruction :", lvcarea, "") + queasy.char1 + chr_unicode(10) + translateExtended ("Proceed with the Room Transfer?", lvcarea, "")

    elif fl_code == 2:

        queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(code))]})

        if queasy and queasy.logi1:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("CASH BASIS Billing Instruction :", lvcarea, "") + queasy.char1 + chr_unicode(10) + translateExtended ("Room Transfer not possible", lvcarea, "")

            return generate_output()

    bill = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"flag": [(eq, 0)]})

    # Rd 21/7/2025
    # if available
    if bill is None:
        return generate_output()
    
    bilrecid = bill._recid
    check_creditlimit()
    check_discrepancy()

    return generate_output()