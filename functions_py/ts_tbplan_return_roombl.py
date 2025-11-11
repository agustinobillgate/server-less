#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.ts_table_check_creditlimitbl import ts_table_check_creditlimitbl
from models import Res_line, Queasy, Htparam, Guest, Mc_guest, Bill

def ts_tbplan_return_roombl(pvilanguage:int, mc_pos1:int, mc_pos2:int, room:string, curr_room:string):

    prepare_cache ([Res_line, Queasy, Htparam, Guest, Bill])

    resnr1 = 0
    reslinnr1 = 0
    gname = ""
    resrecid = 0
    fl_code = 0
    remark = ""
    klimit = to_decimal("0.0")
    ksaldo = to_decimal("0.0")
    hoga_resnr = 0
    hoga_reslinnr = 0
    msg_str = ""
    lvcarea:string = "TS-tbplan"
    res_line = queasy = htparam = guest = mc_guest = bill = None

    resline = None

    Resline = create_buffer("Resline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resnr1, reslinnr1, gname, resrecid, fl_code, remark, klimit, ksaldo, hoga_resnr, hoga_reslinnr, msg_str, lvcarea, res_line, queasy, htparam, guest, mc_guest, bill
        nonlocal pvilanguage, mc_pos1, mc_pos2, room, curr_room
        nonlocal resline


        nonlocal resline

        return {"mc_pos1": mc_pos1, "mc_pos2": mc_pos2, "room": room, "curr_room": curr_room, "resnr1": resnr1, "reslinnr1": reslinnr1, "gname": gname, "resrecid": resrecid, "fl_code": fl_code, "remark": remark, "klimit": klimit, "ksaldo": ksaldo, "hoga_resnr": hoga_resnr, "hoga_reslinnr": hoga_reslinnr, "msg_str": msg_str}

    def check_creditlimit():

        nonlocal resnr1, reslinnr1, gname, resrecid, fl_code, remark, klimit, ksaldo, hoga_resnr, hoga_reslinnr, msg_str, lvcarea, res_line, queasy, htparam, guest, mc_guest, bill
        nonlocal pvilanguage, mc_pos1, mc_pos2, room, curr_room
        nonlocal resline


        nonlocal resline

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
        remark = remark + to_string(res_line.ankunft) + " - " + to_string(res_line.abreise) + chr_unicode(10) + "A " + to_string(res_line.erwachs + res_line.gratis) + " Ch " + to_string(res_line.kind1) + " - " + res_line.arrangement + chr_unicode(10) + res_line.bemerk

    if length(room) > 5:

        if mc_pos1 == 0:
            mc_pos1 = 1

        if mc_pos2 == 0 or mc_pos2 < mc_pos1:
            mc_pos2 = mc_pos1 + length(room) - 1
        mc_pos2 = mc_pos2 - mc_pos1 + 1
        room = substring(room, mc_pos1 - 1, mc_pos2)

        res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"pin_code": [(eq, room)],"resstatus": [(ne, 12)]})

        if not res_line:

            queasy = get_cache (Queasy, {"key": [(eq, 16)],"char1": [(eq, room)]})

            if queasy:

                res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"resnr": [(eq, queasy.number1)],"reslinnr": [(eq, queasy.number2)]})

        if res_line:
            resrecid = res_line._recid
            klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(resrecid))

            if res_line.code != "":

                queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code.strip()))]})

                if queasy and queasy.logi1:
                    msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
            resnr1 = res_line.resnr
            reslinnr1 = res_line.reslinnr
            hoga_resnr = res_line.resnr
            hoga_reslinnr = res_line.reslinnr
            room = res_line.zinr
            gname = res_line.name
            curr_room = room
            fl_code = 1

            return generate_output()

    res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, room)],"resstatus": [(ne, 12)]})

    if res_line:

        if (room.lower()  != (curr_room).lower()):
            resrecid = res_line._recid

            resline = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, room)],"resstatus": [(ne, 12)],"_recid": [(ne, resrecid)]})

            if not resline:
                gname = res_line.name
            else:
                fl_code = 2

                return generate_output()

            if room == "" or resrecid == 0:
                pass
            else:

                res_line = get_cache (Res_line, {"_recid": [(eq, resrecid)]})
                klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(resrecid))

                if res_line.code != "":

                    queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code.strip()))]})

                    if queasy and queasy.logi1:
                        msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
                resnr1 = res_line.resnr
                reslinnr1 = res_line.reslinnr
                gname = res_line.name
                fl_code = 1
        else:
            fl_code = 3

            return generate_output()
    else:
        fl_code = 4

        return generate_output()

    return generate_output()