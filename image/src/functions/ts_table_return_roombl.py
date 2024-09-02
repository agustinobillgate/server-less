from functions.additional_functions import *
import decimal
from sqlalchemy import func
from functions.ts_table_check_creditlimitbl import ts_table_check_creditlimitbl
from functions.ts_pguest import ts_pguest
from models import Res_line, H_bill, Queasy, Zimmer

def ts_table_return_roombl(room:str, mc_pos1:int, mc_pos2:int, gname:str, tischnr:int, dept:int, pvilanguage:int):
    klimit = 0
    ksaldo = 0
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
    lvcarea:str = "TS_table"
    res_line = h_bill = queasy = zimmer = None

    resline = None

    Resline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal klimit, ksaldo, remark, msg_flag, curr_gname, resnr1, reslinnr1, hostnr, hoga_resnr, hoga_reslinnr, curr_room, resrecid, msg_str, err_code, lvcarea, res_line, h_bill, queasy, zimmer
        nonlocal resline


        nonlocal resline
        return {"klimit": klimit, "ksaldo": ksaldo, "remark": remark, "msg_flag": msg_flag, "curr_gname": curr_gname, "resnr1": resnr1, "reslinnr1": reslinnr1, "hostnr": hostnr, "hoga_resnr": hoga_resnr, "hoga_reslinnr": hoga_reslinnr, "curr_room": curr_room, "resrecid": resrecid, "msg_str": msg_str, "err_code": err_code}


    h_bill = db_session.query(H_bill).filter(
            (H_bill.tischnr == tischnr) &  (H_bill.departement == dept)).first()
    curr_gname = gname

    if room == "":
        resnr1 = 0
        reslinnr1 = 0
        hostnr = 0
        err_code = 1

        return generate_output()
    else:

        if len(room) > 5:

            if mc_pos1 == 0:
                mc_pos1 = 1

            if mc_pos2 == 0 or mc_pos2 < mc_pos1:
                mc_pos2 = mc_pos1 + len(room) - 1
            mc_pos2 = mc_pos2 - mc_pos1 + 1
            room = substring(room, mc_pos1 - 1, mc_pos2)

            res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag == 1) &  (func.lower(Res_line.pin_code) == (room).lower()) &  (Res_line.resstatus != 12)).first()

            if not res_line:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 16) &  (func.lower(Queasy.char1) == (room).lower())).first()

                if queasy:

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resnr == queasy.number1) &  (Res_line.reslinnr == queasy.number2)).first()

            if res_line:
                klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(resrecid))

                if res_line.code != "":

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                    if queasy and queasy.logi1:
                        msg_str = msg_str + chr(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
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

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (func.lower(Res_line.zinr) == (room).lower()) &  (Res_line.resstatus != 12)).first()

        if res_line:

            if (room != curr_room):
                resrecid = res_line._recid

                resline = db_session.query(Resline).filter(
                        (Resline.active_flag == 1) &  (func.lower(Resline.zinr) == (room).lower()) &  (Resline.resstatus != 12) &  (Resline._recid != resrecid)).first()

                if not resline:
                    gname = res_line.name
                else:
                    room, gname, resrecid = get_output(ts_pguest(room, gname, resrecid))

                if room == "" or resrecid == 0:
                    room = curr_room
                    err_code = 3

                    return generate_output()
                else:

                    res_line = db_session.query(Res_line).filter(
                            (Res_line._recid == resrecid)).first()
                    klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(resrecid))

                    if res_line.code != "":

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                        if queasy and queasy.logi1:
                            msg_str = msg_str + chr(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
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

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == h_bill.resnr) &  (Res_line.reslinnr == h_bill.reslinnr)).first()

                if res_line:
                    room = res_line.zinr
            else:

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == curr_room)).first()

                if zimmer:
                    room = curr_room
            err_code = 6

            return generate_output()