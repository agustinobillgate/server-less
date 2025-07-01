#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Queasy, Htparam, Guest, Mc_guest, Bill

def ts_tbplan_btn_roombl(pvilanguage:int, resrecid:int):

    prepare_cache ([Res_line, Queasy, Htparam, Guest, Bill])

    resnr1 = 0
    reslinnr1 = 0
    room = ""
    gname = ""
    remark = ""
    klimit = to_decimal("0.0")
    ksaldo = to_decimal("0.0")
    msg_str = ""
    resline = False
    hoga_resnr = 0
    hoga_reslinnr = 0
    lvcarea:string = "TS-tbplan"
    i:int = 0
    str:string = ""
    child_age:string = ""
    res_line = queasy = htparam = guest = mc_guest = bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resnr1, reslinnr1, room, gname, remark, klimit, ksaldo, msg_str, resline, hoga_resnr, hoga_reslinnr, lvcarea, i, str, child_age, res_line, queasy, htparam, guest, mc_guest, bill
        nonlocal pvilanguage, resrecid

        return {"resnr1": resnr1, "reslinnr1": reslinnr1, "room": room, "gname": gname, "remark": remark, "klimit": klimit, "ksaldo": ksaldo, "msg_str": msg_str, "resline": resline, "hoga_resnr": hoga_resnr, "hoga_reslinnr": hoga_reslinnr}

    def check_creditlimit():

        nonlocal resnr1, reslinnr1, room, gname, remark, klimit, ksaldo, msg_str, resline, hoga_resnr, hoga_reslinnr, lvcarea, i, str, child_age, res_line, queasy, htparam, guest, mc_guest, bill
        nonlocal pvilanguage, resrecid

        answer:bool = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 68)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)],"activeflag": [(eq, True)]})

        if mc_guest:
            remark = translateExtended ("Membership No:", lvcarea, "") +\
                " " + mc_guest.cardnum + chr_unicode(10)

        if guest.kreditlimit != 0:
            klimit =  to_decimal(guest.kreditlimit)
        else:

            if htparam.fdecimal != 0:
                klimit =  to_decimal(htparam.fdecimal)
            else:
                klimit =  to_decimal(htparam.finteger)
        ksaldo =  to_decimal("0")

        bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"flag": [(eq, 0)],"zinr": [(eq, res_line.zinr)]})

        if bill:
            ksaldo =  to_decimal(bill.saldo)
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 5) == ("ChAge").lower() :
                child_age = substring(str, 5)

        if child_age != "":
            remark = remark + to_string(res_line.ankunft) + " - " + to_string(res_line.abreise) + chr_unicode(10) + "A:" + to_string(res_line.erwachs + res_line.gratis) + " Ch:" + to_string(res_line.kind1) + " " + "(" + child_age + ")" + " - " + res_line.arrangement + chr_unicode(10) + res_line.bemerk
        else:
            remark = remark + to_string(res_line.ankunft) + " - " + to_string(res_line.abreise) + chr_unicode(10) + "A:" + to_string(res_line.erwachs + res_line.gratis) + " Ch:" + to_string(res_line.kind1) + " - " + res_line.arrangement + chr_unicode(10) + res_line.bemerk

    res_line = get_cache (Res_line, {"_recid": [(eq, resrecid)]})

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

            queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

            if queasy and queasy.logi1:
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1

        return generate_output()

    return generate_output()