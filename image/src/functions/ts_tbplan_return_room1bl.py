from functions.additional_functions import *
import decimal
from models import Res_line, Htparam, Guest, Mc_guest, Bill

def ts_tbplan_return_room1bl(pvilanguage:int, resrecid:int):
    resnr1 = 0
    reslinnr1 = 0
    gname = ""
    remark = ""
    klimit = 0
    ksaldo = 0
    lvcarea:str = "TS_tbplan"
    i:int = 0
    str:str = ""
    child_age:str = ""
    res_line = htparam = guest = mc_guest = bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resnr1, reslinnr1, gname, remark, klimit, ksaldo, lvcarea, i, str, child_age, res_line, htparam, guest, mc_guest, bill


        return {"resnr1": resnr1, "reslinnr1": reslinnr1, "gname": gname, "remark": remark, "klimit": klimit, "ksaldo": ksaldo}

    def check_creditlimit():

        nonlocal resnr1, reslinnr1, gname, remark, klimit, ksaldo, lvcarea, i, str, child_age, res_line, htparam, guest, mc_guest, bill

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
    check_creditlimit()
    resnr1 = res_line.resnr
    reslinnr1 = res_line.reslinnr
    gname = res_line.name

    return generate_output()