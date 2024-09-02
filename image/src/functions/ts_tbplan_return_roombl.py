from functions.additional_functions import *
import decimal
from sqlalchemy import func
from functions.ts_table_check_creditlimitbl import ts_table_check_creditlimitbl
from models import Res_line, Queasy, Htparam, Guest, Mc_guest, Bill

def ts_tbplan_return_roombl(pvilanguage:int, mc_pos1:int, mc_pos2:int, room:str, curr_room:str):
    resnr1 = 0
    reslinnr1 = 0
    gname = ""
    resrecid = 0
    fl_code = 0
    remark = ""
    klimit = 0
    ksaldo = 0
    hoga_resnr = 0
    hoga_reslinnr = 0
    msg_str = ""
    lvcarea:str = "TS_tbplan"
    res_line = queasy = htparam = guest = mc_guest = bill = None

    resline = None

    Resline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resnr1, reslinnr1, gname, resrecid, fl_code, remark, klimit, ksaldo, hoga_resnr, hoga_reslinnr, msg_str, lvcarea, res_line, queasy, htparam, guest, mc_guest, bill
        nonlocal resline


        nonlocal resline
        return {"resnr1": resnr1, "reslinnr1": reslinnr1, "gname": gname, "resrecid": resrecid, "fl_code": fl_code, "remark": remark, "klimit": klimit, "ksaldo": ksaldo, "hoga_resnr": hoga_resnr, "hoga_reslinnr": hoga_reslinnr, "msg_str": msg_str}

    def check_creditlimit():

        nonlocal resnr1, reslinnr1, gname, resrecid, fl_code, remark, klimit, ksaldo, hoga_resnr, hoga_reslinnr, msg_str, lvcarea, res_line, queasy, htparam, guest, mc_guest, bill
        nonlocal resline


        nonlocal resline

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
        remark = remark + to_string(res_line.ankunft) + " - " + to_string(res_line.abreise) + chr(10) + "A " + to_string(res_line.erwachs + res_line.gratis) + "  Ch " + to_string(res_line.kind1) + " - " + res_line.arrangement + chr(10) + res_line.bemerk


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
            resrecid = res_line._recid
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
            fl_code = 1

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
                fl_code = 2

                return generate_output()

            if room == "" or resrecid == 0:
                1
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
                gname = res_line.name
                fl_code = 1
        else:
            fl_code = 3

            return generate_output()
    else:
        fl_code = 4

        return generate_output()