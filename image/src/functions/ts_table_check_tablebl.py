from functions.additional_functions import *
import decimal
from functions.ts_table_check_creditlimitbl import ts_table_check_creditlimitbl
from sqlalchemy import func
from models import H_bill, Kellner, Tisch, Res_line, Queasy, Htparam, Zimmer

def ts_table_check_tablebl(curr_tisch:int, mc_pos1:int, mc_pos2:int, curr_room:str, room:str, pax:int, gname:str, pvilanguage:int, tischnr:int, dept:int, curr_waiter:int, curr_cursor:str, resrecid:int, hostnr:int):
    klimit = 0
    ksaldo = 0
    remark = ""
    table_ok = False
    person = 0
    rmno = ""
    bname = ""
    resnr1 = 0
    reslinnr1 = 0
    hoga_resnr = 0
    hoga_reslinnr = 0
    msg_str = ""
    curr_gname = ""
    err_code = 0
    msg_str2 = ""
    check_flag:bool = False
    lvcarea:str = "TS_table"
    h_bill = kellner = tisch = res_line = queasy = htparam = zimmer = None

    buff_hbill = h_bill1 = resline = None

    Buff_hbill = H_bill
    H_bill1 = H_bill
    Resline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal klimit, ksaldo, remark, table_ok, person, rmno, bname, resnr1, reslinnr1, hoga_resnr, hoga_reslinnr, msg_str, curr_gname, err_code, msg_str2, check_flag, lvcarea, h_bill, kellner, tisch, res_line, queasy, htparam, zimmer
        nonlocal buff_hbill, h_bill1, resline


        nonlocal buff_hbill, h_bill1, resline
        return {"klimit": klimit, "ksaldo": ksaldo, "remark": remark, "table_ok": table_ok, "person": person, "rmno": rmno, "bname": bname, "resnr1": resnr1, "reslinnr1": reslinnr1, "hoga_resnr": hoga_resnr, "hoga_reslinnr": hoga_reslinnr, "msg_str": msg_str, "curr_gname": curr_gname, "err_code": err_code, "msg_str2": msg_str2}

    def check_table():

        nonlocal klimit, ksaldo, remark, table_ok, person, rmno, bname, resnr1, reslinnr1, hoga_resnr, hoga_reslinnr, msg_str, curr_gname, err_code, msg_str2, check_flag, lvcarea, h_bill, kellner, tisch, res_line, queasy, htparam, zimmer
        nonlocal buff_hbill, h_bill1, resline


        nonlocal buff_hbill, h_bill1, resline

        billno:int = 0
        H_bill1 = H_bill
        check_flag = True

        h_bill1 = db_session.query(H_bill1).filter(
                (H_bill1.tischnr == tischnr) &  (H_bill1.departement == dept) &  (H_bill1.flag == 0)).first()

        if not kellner.masterkey:

            if h_bill1 and h_bill1.kellner_nr != curr_waiter:
                table_ok = False

            elif tisch.kellner_nr != 0 and tisch.kellner_nr != curr_waiter:
                table_ok = False

            if not table_ok:
                msg_str = msg_str + chr(2) + translateExtended ("This table belongs to other waiter.", lvcarea, "")
                err_code = 2

                return

        if h_bill1:
            person = h_bill1.belegung
            bname = h_bill1.bilname

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == h_bill1.resnr) &  (Res_line.reslinnr == h_bill1.reslinnr)).first()

            if res_line:
                klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(res_line._recid))

                if res_line.code != "":

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                    if queasy and queasy.logi1:
                        msg_str2 = msg_str2 + chr(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
                rmno = res_line.zinr
                resnr1 = h_bill1.resnr
                reslinnr1 = h_bill1.reslinnr
                hoga_resnr = h_bill1.resnr
                hoga_reslinnr = h_bill1.resnr


            bname = h_bill1.bilname
        else:
            person = tisch.normalbeleg
            rmno = ""
            gname = ""
            hoga_resnr = 0
            hoga_reslinnr = 0
        curr_tisch = tischnr

    def return_room():

        nonlocal klimit, ksaldo, remark, table_ok, person, rmno, bname, resnr1, reslinnr1, hoga_resnr, hoga_reslinnr, msg_str, curr_gname, err_code, msg_str2, check_flag, lvcarea, h_bill, kellner, tisch, res_line, queasy, htparam, zimmer
        nonlocal buff_hbill, h_bill1, resline


        nonlocal buff_hbill, h_bill1, resline


        Resline = Res_line

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 253)).first()

        if tischnr == 0:
            room = ""
            err_code = 3

            return
        else:

            h_bill = db_session.query(H_bill).filter(
                    (H_bill.tischnr == tischnr) &  (H_bill.departement == dept)).first()
            curr_gname = gname

            if room == "":
                resnr1 = 0
                reslinnr1 = 0
                hostnr = 0
                err_code = 4

                return
            else:

                if len(room) > 5:

                    if mc_pos1 == 0:
                        mc_pos1 = 1

                    if mc_pos2 == 0 or mc_pos2 < mc_pos1:
                        mc_pos2 = mc_pos1 + len(room) - 1
                    mc_pos2 = mc_pos2 - mc_pos1 + 1
                    room = substring(room, mc_pos1 - 1, mc_pos2)

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.active_flag == 1) &  (func.lower(Res_line.pin_code) == (room).lower()) &  (Res_line.resstatus == 6)).first()

                    if not res_line:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 16) &  (func.lower(Queasy.char1) == (room).lower())).first()

                        if queasy:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.active_flag == 1) &  (Res_line.resnr == queasy.number1) &  (Res_line.reslinnr == queasy.number2)).first()

                    if res_line:
                        klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(res_line._recid))

                        if res_line.code != "":

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                            if queasy and queasy.logi1:
                                msg_str2 = msg_str2 + chr(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
                        resnr1 = res_line.resnr
                        reslinnr1 = res_line.reslinnr
                        hoga_resnr = res_line.resnr
                        hoga_reslinnr = res_line.reslinnr
                        room = res_line.zinr
                        gname = res_line.name
                        curr_room = room
                        curr_gname = gname
                        err_code = 5

                        return

                res_line = db_session.query(Res_line).filter(
                        (Res_line.active_flag == 1) &  (func.lower(Res_line.zinr) == (room).lower()) &  (Res_line.resstatus == 6)).first()

                if res_line:

                    if (room != curr_room):
                        resrecid = res_line._recid

                        resline = db_session.query(Resline).filter(
                                (Resline.active_flag == 1) &  (func.lower(Resline.zinr) == (room).lower()) &  (res_line.resstatus == 6) &  (Resline._recid != resrecid)).first()

                        if not resline:
                            gname = res_line.name

                        if room == "" or resrecid == 0:
                            room = curr_room
                            err_code = 6

                            return
                        else:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line._recid == resrecid)).first()
                            klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(resrecid))

                            if res_line.code != "":

                                queasy = db_session.query(Queasy).filter(
                                        (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                                if queasy and queasy.logi1:
                                    msg_str2 = msg_str2 + chr(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
                            resnr1 = res_line.resnr
                            reslinnr1 = res_line.reslinnr
                            hoga_resnr = res_line.resnr
                            hoga_reslinnr = res_line.reslinnr
                            gname = res_line.name
                            curr_room = room
                            curr_gname = gname
                            err_code = 7

                            return
                    else:
                        resnr1 = res_line.resnr
                        reslinnr1 = res_line.reslinnr
                        hoga_resnr = res_line.resnr
                        hoga_reslinnr = res_line.reslinnr
                        gname = res_line.name


                        err_code = 8

                        return
                else:
                    room = ""

                    if h_bill and h_bill.resnr > 0:

                        res_line = db_session.query(Res_line).filter(
                                (Res_line.resnr == h_bill.resnr) &  (Res_line.reslinnr == h_bill.reslinnr)).first()

                        if res_line:
                            room = res_line.zinr
                    else:

                        zimmer = db_session.query(Zimmer).filter(
                                (func.lower(Zimmer.zinr) == (curr_room).lower())).first()

                        if zimmer:
                            room = curr_room
                    err_code = 9

                    return


    kellner = db_session.query(Kellner).filter(
            (Kellner_nr == curr_waiter) &  (Kellner.departement == dept)).first()

    tisch = db_session.query(Tisch).filter(
            (tischnr == tischnr) &  (Tisch.departement == dept)).first()
    check_flag = False
    check_table()

    if not table_ok:
        tischnr = 0
        pax = 0
        room = ""
        gname = ""
        err_code = 1

        return generate_output()

    if table_ok:

        if curr_cursor.lower()  == "tischnr" or curr_cursor.lower()  == "pax":
            pax = person
            room = rmno
            gname = bname

    if table_ok and curr_cursor.lower()  == "pax" and person != 0:
        pax = person

    if curr_room.lower()  != (room).lower() :
        return_room()

    h_bill = db_session.query(H_bill).filter(
            (H_bill.tischnr == tischnr) &  (H_bill.departement == dept) &  (H_bill.flag == 0)).first()

    if h_bill:

        h_bill = db_session.query(H_bill).first()
        h_bill.service[1] = hostnr
        h_bill.belegung = pax
        h_bill.bilname = gname

        if check_flag:
            h_bill.resnr = resnr1
            h_bill.reslinnr = reslinnr1

        h_bill = db_session.query(H_bill).first()

    return generate_output()