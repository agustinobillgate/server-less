from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpdate import htpdate
from models import Htparam, Bill, Res_line, Queasy, Guest

def prepare_ts_rzinrbl(pvilanguage:int, dept:int, zinr:str, h_resnr:int, h_reslinnr:int, balance:decimal):
    dept_mbar = 0
    dept_ldry = 0
    bilrecid = 0
    mc_pos1 = 0
    mc_pos2 = 0
    mc_flag = False
    fl_code = 0
    msg_str = ""
    msg_str2 = ""
    q1_list_list = []
    lvcarea:str = "TS_rzinr"
    bill_date:date = None
    res_bemerk:str = ""
    loopk:int = 0
    htparam = bill = res_line = queasy = guest = None

    q1_list = bbuff = None

    q1_list_list, Q1_list = create_model("Q1_list", {"resnr":int, "zinr":str, "code":str, "resstatus":int, "erwachs":int, "kind1":int, "gratis":int, "bemerk":str, "billnr":int, "g_name":str, "vorname1":str, "anrede1":str, "anredefirma":str, "bill_name":str, "ankunft":date, "abreise":date, "nation1":str, "parent_nr":int, "reslinnr":int, "resname":str, "name_bg_col":int, "name_fg_col":int, "bill_bg_col":int, "bill_fg_col":int}, {"name_bg_col": 15, "bill_bg_col": 15})

    Bbuff = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dept_mbar, dept_ldry, bilrecid, mc_pos1, mc_pos2, mc_flag, fl_code, msg_str, msg_str2, q1_list_list, lvcarea, bill_date, res_bemerk, loopk, htparam, bill, res_line, queasy, guest
        nonlocal bbuff


        nonlocal q1_list, bbuff
        nonlocal q1_list_list
        return {"dept_mbar": dept_mbar, "dept_ldry": dept_ldry, "bilrecid": bilrecid, "mc_pos1": mc_pos1, "mc_pos2": mc_pos2, "mc_flag": mc_flag, "fl_code": fl_code, "msg_str": msg_str, "msg_str2": msg_str2, "q1-list": q1_list_list}

    def check_creditlimit():

        nonlocal dept_mbar, dept_ldry, bilrecid, mc_pos1, mc_pos2, mc_flag, fl_code, msg_str, msg_str2, q1_list_list, lvcarea, bill_date, res_bemerk, loopk, htparam, bill, res_line, queasy, guest
        nonlocal bbuff


        nonlocal q1_list, bbuff
        nonlocal q1_list_list

        klimit:decimal = 0

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
            msg_str2 = msg_str2 + chr(2) + "&Q" + translateExtended ("OVER Credit Limit found: ", lvcarea, "") + translateExtended ("Given Limit   == ", lvcarea, "") + " " + trim(to_string(klimit, ">>>,>>>,>>>,>>9")) + " / " + translateExtended ("Bill balance  == ", lvcarea, "") + " " + trim(to_string(bill.saldo, "->>>,>>>,>>>,>>9.99")) + chr(10) + translateExtended ("Restaurant balance  == ", lvcarea, "") + " " + trim(to_string(balance, "->>>,>>>,>>>,>>9.99")) + chr(10) + translateExtended ("Do you wish to CANCEL the room transfer?", lvcarea, "")

    if not CONNECTED ("vhp"):
        msg_str = translateExtended ("DB not connected.", lvcarea, "")
        bilrecid = 0
        fl_code = 2

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 949)).first()

    if htparam.feldtyp == 1:
        dept_mbar = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1081)).first()

    if htparam.feldtyp == 1:
        dept_ldry = htparam.finteger

    bill = db_session.query(Bill).filter(
            (Bill.resnr == h_resnr) &  (Bill.reslinnr == h_reslinnr) &  (Bill.zinr != "") &  (Bill.flag == 0)).first()

    if bill:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == h_resnr) &  (Res_line.reslinnr == h_reslinnr)).first()

        if res_line and res_line.CODE != "":

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

            if queasy and queasy.logi1 and dept != dept_mbar and dept != dept_ldry:
                msg_str = msg_str + chr(2) + translateExtended ("CASH BASIS Billing Instruction :", lvcarea, "") + queasy.char1 + chr(10) + translateExtended ("Room Transfer not possible", lvcarea, "")
                bilrecid = 0
                fl_code = 1

                return generate_output()

        if bill.flag == 0:
            bilrecid = bill._recid
            check_creditlimit()
            fl_code = -1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 336)).first()

    if htparam.feldtyp == 4:
        mc_flag = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 337)).first()
        mc_pos1 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 338)).first()
        mc_pos2 = htparam.finteger

    res_line_obj_list = []
    for res_line, guest, bbuff in db_session.query(Res_line, Guest, Bbuff).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Bbuff,(Bbuff.resnr == Res_line.resnr) &  (Bbuff.reslinnr == Res_line.reslinnr)).filter(
            (Res_line.active_flag == 1) &  (func.lower(Res_line.(zinr).lower()) >= (zinr).lower())).all():
        if res_line._recid in res_line_obj_list:
            continue
        else:
            res_line_obj_list.append(res_line._recid)


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.resnr = res_line.resnr
        q1_list.zinr = res_line.zinr
        q1_list.code = res_line.code
        q1_list.resstatus = res_line.resstatus
        q1_list.erwachs = res_line.erwachs
        q1_list.kind1 = res_line.kind1
        q1_list.gratis = res_line.gratis
        q1_list.bemerk = res_line.bemerk
        q1_list.billnr = bbuff.billnr
        q1_list.g_name = guest.name
        q1_list.vorname1 = guest.vorname1
        q1_list.anrede1 = guest.anrede1
        q1_list.anredefirma = guest.anredefirma
        q1_list.bill_name = bbuff.name
        q1_list.ankunft = res_line.ankunft
        q1_list.abreise = res_line.abreise
        q1_list.nation1 = guest.nation1
        q1_list.parent_nr = bbuff.parent_nr
        q1_list.reslinnr = res_line.reslinnr
        q1_list.resname = res_line.name

        if (dept != dept_mbar and dept != dept_ldry):

            if res_line.code != "":

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                if queasy and queasy.logi1:
                    q1_list.name_bg_col = 12
                    q1_list.name_fg_col = 15

        if res_line.resstatus == 12:
            q1_list.bill_bg_col = 2
            q1_list.bill_fg_col = 15


        q1_list.bemerk = replace_str(q1_list.bemerk, chr(10) , "")


        q1_list.bemerk = replace_str(q1_list.bemerk, chr(13) , "")
        q1_list.bemerk = replace_str(q1_list.bemerk, "~n", "")
        q1_list.bemerk = replace_str(q1_list.bemerk, "\\n", "")
        q1_list.bemerk = replace_str(q1_list.bemerk, "~r", "")
        q1_list.bemerk = replace_str(q1_list.bemerk, "~r~n", "")
        q1_list.bemerk = replace_str(q1_list.bemerk, chr(10) + chr(13) , "")
        res_bemerk = ""
        for loopk in range(1,len(q1_list.bemerk)  + 1) :

            if ord(substring(q1_list.bemerk, loopk - 1, 1)) == 0:
                pass
            else:
                res_bemerk = res_bemerk + substring(q1_list.bemerk, loopk - 1, 1)
        q1_list.bemerk = res_bemerk

        if len(q1_list.bemerk) < 3:
            q1_list.bemerk = replace_str(q1_list.bemerk, chr(32) , "")

        if len(q1_list.bemerk) == None:
            q1_list.bemerk = ""

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 974)).first()

    if not htparam.flogical:

        return generate_output()
    bill_date = get_output(htpdate(110))

    res_line_obj_list = []
    for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
            (Res_line.resstatus == 8) &  (Res_line.abreise == bill_date) &  (Res_line.l_zuordnung[2] == 0) &  (func.lower(Res_line.(zinr).lower()) >= (zinr).lower())).all():
        if res_line._recid in res_line_obj_list:
            continue
        else:
            res_line_obj_list.append(res_line._recid)

        for bbuff in db_session.query(Bbuff).filter(
                (Bbuff.resnr == res_line.resnr) &  (Bbuff.parent_nr == res_line.reslinnr) &  (Bbuff.saldo != 0)).all():
            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            q1_list.resnr = res_line.resnr
            q1_list.zinr = res_line.zinr
            q1_list.code = res_line.code
            q1_list.resstatus = res_line.resstatus
            q1_list.erwachs = res_line.erwachs
            q1_list.kind1 = res_line.kind1
            q1_list.gratis = res_line.gratis
            q1_list.bemerk = res_line.bemerk
            q1_list.billnr = bbuff.billnr
            q1_list.g_name = guest.name
            q1_list.vorname1 = guest.vorname1
            q1_list.anrede1 = guest.anrede1
            q1_list.anredefirma = guest.anredefirma
            q1_list.bill_name = bbuff.name
            q1_list.ankunft = res_line.ankunft
            q1_list.abreise = res_line.abreise
            q1_list.nation1 = guest.nation1
            q1_list.parent_nr = bbuff.parent_nr
            q1_list.reslinnr = res_line.reslinnr
            q1_list.resname = res_line.name

            if (dept != dept_mbar and dept != dept_ldry):

                if res_line.code != "":

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

                    if queasy and queasy.logi1:
                        q1_list.name_bg_col = 12
                        q1_list.name_fg_col = 15


            q1_list.bemerk = replace_str(q1_list.bemerk, chr(10) , "")


            q1_list.bemerk = replace_str(q1_list.bemerk, chr(13) , "")
            q1_list.bemerk = replace_str(q1_list.bemerk, "~n", "")
            q1_list.bemerk = replace_str(q1_list.bemerk, "\\n", "")
            q1_list.bemerk = replace_str(q1_list.bemerk, "~r", "")
            q1_list.bemerk = replace_str(q1_list.bemerk, "~r~n", "")
            q1_list.bemerk = replace_str(q1_list.bemerk, chr(10) + chr(13) , "")
            res_bemerk = ""
            for loopk in range(1,len(q1_list.bemerk)  + 1) :

                if ord(substring(q1_list.bemerk, loopk - 1, 1)) == 0:
                    pass
                else:
                    res_bemerk = res_bemerk + substring(q1_list.bemerk, loopk - 1, 1)
            q1_list.bemerk = res_bemerk

            if len(q1_list.bemerk) < 3:
                q1_list.bemerk = replace_str(q1_list.bemerk, chr(32) , "")

            if len(q1_list.bemerk) == None:
                q1_list.bemerk = ""

    return generate_output()