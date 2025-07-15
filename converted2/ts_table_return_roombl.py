#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.ts_table_check_creditlimitbl import ts_table_check_creditlimitbl
from functions.ts_pguest import ts_pguest
from models import Res_line, H_bill, Queasy, Zimmer

def ts_table_return_roombl(room:string, mc_pos1:int, mc_pos2:int, gname:string, tischnr:int, dept:int, pvilanguage:int):

    prepare_cache ([Res_line, H_bill, Queasy])

    klimit = to_decimal("0.0")
    ksaldo = to_decimal("0.0")
    remark = ""
    msg_flag = 0
    curr_gname = ""
    resnr1 = 0
    reslinnr1 = 0
    hostnr = 0
    hoga_resnr = 0
    hoga_reslinnr = 0
    curr_room = ""
    resrecid = 0
    msg_str = ""
    err_code = 0
    lvcarea:string = "TS-table"
    res_line = h_bill = queasy = zimmer = None

    resline = None

    Resline = create_buffer("Resline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal klimit, ksaldo, remark, msg_flag, curr_gname, resnr1, reslinnr1, hostnr, hoga_resnr, hoga_reslinnr, curr_room, resrecid, msg_str, err_code, lvcarea, res_line, h_bill, queasy, zimmer
        nonlocal room, mc_pos1, mc_pos2, gname, tischnr, dept, pvilanguage
        nonlocal resline


        nonlocal resline

        return {"room": room, "mc_pos1": mc_pos1, "mc_pos2": mc_pos2, "gname": gname, "klimit": klimit, "ksaldo": ksaldo, "remark": remark, "msg_flag": msg_flag, "curr_gname": curr_gname, "resnr1": resnr1, "reslinnr1": reslinnr1, "hostnr": hostnr, "hoga_resnr": hoga_resnr, "hoga_reslinnr": hoga_reslinnr, "curr_room": curr_room, "resrecid": resrecid, "msg_str": msg_str, "err_code": err_code}


    h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, dept)]})
    curr_gname = gname

    if room == "":
        resnr1 = 0
        reslinnr1 = 0
        hostnr = 0
        err_code = 1

        return generate_output()
    else:

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
                klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(resrecid))

                if res_line.code != "":

                    queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                    if queasy and queasy.logi1:
                        msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
                resnr1 = res_line.resnr
                reslinnr1 = res_line.reslinnr
                hoga_resnr = res_line.resnr
                hoga_reslinnr = res_line.reslinnr
                room = res_line.zinr
                gname = res_line.name
                curr_room = room
                curr_gname = gname
                err_code = 2

                return generate_output()

        res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, room)],"resstatus": [(ne, 12)]})

        if res_line:

            if (room.lower()  != (curr_room).lower()):
                resrecid = res_line._recid

                resline = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, room)],"resstatus": [(ne, 12)],"_recid": [(ne, resrecid)]})

                if not resline:
                    gname = res_line.name
                else:
                    room, gname, resrecid = get_output(ts_pguest(room, gname, resrecid))

                if room == "" or resrecid == 0:
                    room = curr_room
                    err_code = 3

                    return generate_output()
                else:

                    res_line = get_cache (Res_line, {"_recid": [(eq, resrecid)]})
                    klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(resrecid))

                    if res_line.code != "":

                        queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                        if queasy and queasy.logi1:
                            msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
                    resnr1 = res_line.resnr
                    reslinnr1 = res_line.reslinnr
                    hoga_resnr = res_line.resnr
                    hoga_reslinnr = res_line.reslinnr
                    gname = res_line.name
                    curr_room = room
                    curr_gname = gname
                    err_code = 4

                    return generate_output()
            else:
                err_code = 5

                return generate_output()
        else:
            msg_flag = 1
            room = ""

            if h_bill and h_bill.resnr > 0:

                res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                if res_line:
                    room = res_line.zinr
            else:

                zimmer = get_cache (Zimmer, {"zinr": [(eq, curr_room)]})

                if zimmer:
                    room = curr_room
            err_code = 6

            return generate_output()

    return generate_output()