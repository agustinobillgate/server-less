#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.ts_table_check_creditlimitbl import ts_table_check_creditlimitbl
from models import H_bill, Kellner, Tisch, Res_line, Queasy, Htparam, Zimmer

def ts_table_check_tablebl(curr_tisch:int, mc_pos1:int, mc_pos2:int, curr_room:string, room:string, pax:int, gname:string, pvilanguage:int, tischnr:int, dept:int, curr_waiter:int, curr_cursor:string, resrecid:int, hostnr:int):

    prepare_cache ([H_bill, Tisch, Res_line, Queasy])

    klimit = to_decimal("0.0")
    ksaldo = to_decimal("0.0")
    remark = ""
    table_ok = True
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
    lvcarea:string = "TS-table"
    h_bill = kellner = tisch = res_line = queasy = htparam = zimmer = None

    buff_hbill = None

    Buff_hbill = create_buffer("Buff_hbill",H_bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal klimit, ksaldo, remark, table_ok, person, rmno, bname, resnr1, reslinnr1, hoga_resnr, hoga_reslinnr, msg_str, curr_gname, err_code, msg_str2, check_flag, lvcarea, h_bill, kellner, tisch, res_line, queasy, htparam, zimmer
        nonlocal curr_tisch, mc_pos1, mc_pos2, curr_room, room, pax, gname, pvilanguage, tischnr, dept, curr_waiter, curr_cursor, resrecid, hostnr
        nonlocal buff_hbill


        nonlocal buff_hbill

        return {"curr_tisch": curr_tisch, "mc_pos1": mc_pos1, "mc_pos2": mc_pos2, "curr_room": curr_room, "room": room, "pax": pax, "gname": gname, "klimit": klimit, "ksaldo": ksaldo, "remark": remark, "table_ok": table_ok, "person": person, "rmno": rmno, "bname": bname, "resnr1": resnr1, "reslinnr1": reslinnr1, "hoga_resnr": hoga_resnr, "hoga_reslinnr": hoga_reslinnr, "msg_str": msg_str, "curr_gname": curr_gname, "err_code": err_code, "msg_str2": msg_str2}

    def check_table():

        nonlocal klimit, ksaldo, remark, table_ok, person, rmno, bname, resnr1, reslinnr1, hoga_resnr, hoga_reslinnr, msg_str, curr_gname, err_code, msg_str2, check_flag, lvcarea, h_bill, kellner, tisch, res_line, queasy, htparam, zimmer
        nonlocal curr_tisch, mc_pos1, mc_pos2, curr_room, room, pax, gname, pvilanguage, tischnr, dept, curr_waiter, curr_cursor, resrecid, hostnr
        nonlocal buff_hbill


        nonlocal buff_hbill

        billno:int = 0
        h_bill1 = None
        H_bill1 =  create_buffer("H_bill1",H_bill)
        check_flag = True

        h_bill1 = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, dept)],"flag": [(eq, 0)]})

        if not kellner.masterkey:

            if h_bill1 and h_bill1.kellner_nr != curr_waiter:
                table_ok = False

            elif tisch.kellner_nr != 0 and tisch.kellner_nr != curr_waiter:
                table_ok = False

            if not table_ok:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("This table belongs to other waiter.", lvcarea, "")
                err_code = 2

                return

        if h_bill1:
            person = h_bill1.belegung
            bname = h_bill1.bilname

            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill1.resnr)],"reslinnr": [(eq, h_bill1.reslinnr)]})

            if res_line:
                klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(res_line._recid))

                if res_line.code != "":

                    queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                    if queasy and queasy.logi1:
                        msg_str2 = msg_str2 + chr_unicode(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
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
        nonlocal curr_tisch, mc_pos1, mc_pos2, curr_room, room, pax, gname, pvilanguage, tischnr, dept, curr_waiter, curr_cursor, resrecid, hostnr
        nonlocal buff_hbill


        nonlocal buff_hbill

        resline = None
        Resline =  create_buffer("Resline",Res_line)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

        if tischnr == 0:
            room = ""
            err_code = 3

            return
        else:

            h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, dept)]})
            curr_gname = gname

            if room == "":
                resnr1 = 0
                reslinnr1 = 0
                hostnr = 0
                err_code = 4

                return
            else:

                if length(room) > 5:

                    if mc_pos1 == 0:
                        mc_pos1 = 1

                    if mc_pos2 == 0 or mc_pos2 < mc_pos1:
                        mc_pos2 = mc_pos1 + length(room) - 1
                    mc_pos2 = mc_pos2 - mc_pos1 + 1
                    room = substring(room, mc_pos1 - 1, mc_pos2)

                    res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"pin_code": [(eq, room)],"resstatus": [(eq, 6)]})

                    if not res_line:

                        queasy = get_cache (Queasy, {"key": [(eq, 16)],"char1": [(eq, room)]})

                        if queasy:

                            res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"resnr": [(eq, queasy.number1)],"reslinnr": [(eq, queasy.number2)]})

                    if res_line:
                        klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(res_line._recid))

                        if res_line.code != "":

                            queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                            if queasy and queasy.logi1:
                                msg_str2 = msg_str2 + chr_unicode(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
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

                res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, room)],"resstatus": [(eq, 6)]})

                if res_line:

                    if (room.lower()  != (curr_room).lower()):
                        resrecid = res_line._recid

                        resline = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, room)],"resstatus": [(eq, 6)],"_recid": [(ne, resrecid)]})

                        if not resline:
                            gname = res_line.name

                        if room == "" or resrecid == 0:
                            room = curr_room
                            err_code = 6

                            return
                        else:

                            res_line = get_cache (Res_line, {"_recid": [(eq, resrecid)]})
                            klimit, ksaldo, remark = get_output(ts_table_check_creditlimitbl(resrecid))

                            if res_line.code != "":

                                queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                                if queasy and queasy.logi1:
                                    msg_str2 = msg_str2 + chr_unicode(2) + "&W" + translateExtended ("CASH BASIS Billing Instruction: ", lvcarea, "") + queasy.char1
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

                        res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                        if res_line:
                            room = res_line.zinr
                    else:

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, curr_room)]})

                        if zimmer:
                            room = curr_room
                    err_code = 9

                    return

    kellner = get_cache (Kellner, {"kellner_nr": [(eq, curr_waiter)],"departement": [(eq, dept)]})

    tisch = get_cache (Tisch, {"tischnr": [(eq, tischnr)],"departement": [(eq, dept)]})
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

        if curr_cursor.lower()  == ("tischnr").lower()  or curr_cursor.lower()  == ("pax").lower() :
            pax = person
            room = rmno
            gname = bname

    if table_ok and curr_cursor.lower()  == ("pax").lower()  and person != 0:
        pax = person

    if curr_room.lower()  != (room).lower() :
        return_room()

    h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, dept)],"flag": [(eq, 0)]})

    if h_bill:
        pass
        h_bill.service[1] = hostnr
        h_bill.belegung = pax
        h_bill.bilname = gname

        if check_flag:
            h_bill.resnr = resnr1
            h_bill.reslinnr = reslinnr1


        pass

    return generate_output()