from functions.additional_functions import *
import decimal
from models import Queasy, Bill, Htparam, Guest, Res_line, Zimmer

def ts_rzinr_btn_exitbl(pvilanguage:int, fl_code:int, code:str, resnr:int, reslinnr:int, balance:decimal):
    bilrecid = 0
    msg_str = ""
    msg_str1 = ""
    msg_str2 = ""
    lvcarea:str = "TS_rzinr"
    queasy = bill = htparam = guest = res_line = zimmer = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bilrecid, msg_str, msg_str1, msg_str2, lvcarea, queasy, bill, htparam, guest, res_line, zimmer


        return {"bilrecid": bilrecid, "msg_str": msg_str, "msg_str1": msg_str1, "msg_str2": msg_str2}

    def check_creditlimit():

        nonlocal bilrecid, msg_str, msg_str1, msg_str2, lvcarea, queasy, bill, htparam, guest, res_line, zimmer

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
            msg_str1 = msg_str1 + chr(2) + "&Q" + translateExtended ("OVER Credit Limit found: ", lvcarea, "") + translateExtended ("Given Limit   == ", lvcarea, "") + " " + trim(to_string(klimit, ">>>,>>>,>>>,>>9")) + " / " + translateExtended ("Bill balance  == ", lvcarea, "") + " " + trim(to_string(bill.saldo, "->>>,>>>,>>>,>>9.99")) + chr(10) + translateExtended ("Restaurant balance  == ", lvcarea, "") + " " + trim(to_string(balance, "->>>,>>>,>>>,>>9.99")) + chr(10) + translateExtended ("Do you wish to CANCEL the room transfer?", lvcarea, "")

    def check_discrepancy():

        nonlocal bilrecid, msg_str, msg_str1, msg_str2, lvcarea, queasy, bill, htparam, guest, res_line, zimmer

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

        if res_line:

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == res_line.zinr) &  (Zimmer.house_status != 0)).first()

            if zimmer:
                msg_str2 = translateExtended ("Room discrepancy is found. Transaction not possible.", lvcarea, "") + chr(10) + translateExtended ("Please contact Front Office.", lvcarea, "")


    if fl_code == 1:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 9) &  (Queasy.number1 == to_int(code))).first()

        if queasy and queasy.logi1:
            msg_str = msg_str + chr(2) + "&Q" + translateExtended ("CASH BASIS Billing Instruction :", lvcarea, "") + queasy.char1 + chr(10) + translateExtended ("Proceed with the Room Transfer?", lvcarea, "")

    elif fl_code == 2:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 9) &  (Queasy.number1 == to_int(code))).first()

        if queasy and queasy.logi1:
            msg_str = msg_str + chr(2) + translateExtended ("CASH BASIS Billing Instruction :", lvcarea, "") + queasy.char1 + chr(10) + translateExtended ("Room Transfer not possible", lvcarea, "")

            return generate_output()

    bill = db_session.query(Bill).filter(
            (Bill.resnr == resnr) &  (Bill.reslinnr == reslinnr) &  (Bill.flag == 0)).first()
    bilrecid = bill._recid
    check_creditlimit()
    check_discrepancy()

    return generate_output()