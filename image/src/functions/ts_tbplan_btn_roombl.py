from functions.additional_functions import *
import decimal
from models import Res_line, Queasy, Htparam, Guest, Mc_guest, Bill

def ts_tbplan_btn_roombl(pvilanguage:int, resrecid:int):
    resnr1 = 0
    reslinnr1 = 0
    room = ""
    gname = ""
    remark = ""
    klimit = 0
    ksaldo = 0
    msg_str = ""
    resline = False
    hoga_resnr = 0
    hoga_reslinnr = 0
    lvcarea:str = "TS_tbplan"
    i:int = 0
    str:str = ""
    child_age:str = ""
    res_line = queasy = htparam = guest = mc_guest = bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resnr1, reslinnr1, room, gname, remark, klimit, ksaldo, msg_str, resline, hoga_resnr, hoga_reslinnr, lvcarea, i, str, child_age, res_line, queasy, htparam, guest, mc_guest, bill


        return {"resnr1": resnr1, "reslinnr1": reslinnr1, "room": room, "gname": gname, "remark": remark, "klimit": klimit, "ksaldo": ksaldo, "msg_str": msg_str, "resline": resline, "hoga_resnr": hoga_resnr, "hoga_reslinnr": hoga_reslinnr}

    def check_creditlimit():

        nonlocal resnr1, reslinnr1, room, gname, remark, klimit, ksaldo, msg_str, resline, hoga_resnr, hoga_reslinnr, lvcarea, i, str, child_age, res_line, queasy, htparam, guest, mc_guest, bill

        answer:bool = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 68)).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrpay)).first()

        mc_guest = db_session.query(Mc_guest).filter(
                (Mc_guest.gastnr == guest.gastnr) &  (Mc_guest.activeflag)).first()

        if mc_guest:
            remark = translateExtended ("Membership No:", lvcarea, "") +\
                " " + mc_guest.cardnum + chr(10)

        if guest.kreditlimit != 0:
            klimit = guest.kreditlimit
        else:

            if htparam.fdecimal != 0:
                klimit = htparam.fdecimal
            else:
                klimit = htparam.finteger
        ksaldo = 0

        bill = db_session.query(Bill).filter(
                (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr) &  (Bill.flag == 0) &  (Bill.zinr == res_line.zinr)).first()

        if bill:
            ksaldo = bill.saldo
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 5) == "ChAge":
                child_age = substring(str, 5)

        if child_age != "":
            remark = remark + to_string(res_line.ankunft) + " - " + to_string(res_line.abreise) + chr(10) + "A:" + to_string(res_line.erwachs + res_line.gratis) + " Ch:" + to_string(res_line.kind1) + " " + "(" + child_age + ")" + " - " + res_line.arrangement + chr(10) + res_line.bemerk
        else:
            remark = remark + to_string(res_line.ankunft) + " - " + to_string(res_line.abreise) + chr(10) + "A:" + to_string(res_line.erwachs + res_line.gratis) + " Ch:" + to_string(res_line.kind1) + " - " + res_line.arrangement + chr(10) + res_line.bemerk


    res_line = db_session.query(Res_line).filter(
            (Res_line._recid == resrecid)).first()

    if res_line:
        resline = True
        check_creditlimit()
        resnr1 = res_line.resnr
        reslinnr1 = res_line.reslinnr
        hoga_resnr = res_line.resnr
        hoga_reslinnr = res_line.reslinnr
        room = res_line.zinr
        gname = res_line.name

        if res_line.code != "":

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

            if queasy and queasy.logi1:
                msg_str = msg_str + chr(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1

        return generate_output()