#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Htparam, Bill, Res_line, Queasy, Guest

def prepare_ts_rzinrbl(pvilanguage:int, dept:int, zinr:string, h_resnr:int, h_reslinnr:int, balance:Decimal):

    prepare_cache ([Htparam, Bill, Res_line, Queasy, Guest])

    dept_mbar = 0
    dept_ldry = 0
    bilrecid = 0
    mc_pos1 = 0
    mc_pos2 = 0
    mc_flag = False
    fl_code = 0
    msg_str = ""
    msg_str2 = ""
    q1_list_data = []
    lvcarea:string = "TS-rzinr"
    bill_date:date = None
    res_bemerk:string = ""
    loopk:int = 0
    htparam = bill = res_line = queasy = guest = None

    q1_list = guest2 = bbuff = None

    q1_list_data, Q1_list = create_model("Q1_list", {"resnr":int, "zinr":string, "code":string, "resstatus":int, "erwachs":int, "kind1":int, "gratis":int, "bemerk":string, "billnr":int, "g_name":string, "vorname1":string, "anrede1":string, "anredefirma":string, "bill_name":string, "ankunft":date, "abreise":date, "nation1":string, "parent_nr":int, "reslinnr":int, "resname":string, "name_bg_col":int, "name_fg_col":int, "bill_bg_col":int, "bill_fg_col":int}, {"name_bg_col": 15, "bill_bg_col": 15})

    Guest2 = create_buffer("Guest2",Guest)
    Bbuff = create_buffer("Bbuff",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal dept_mbar, dept_ldry, bilrecid, mc_pos1, mc_pos2, mc_flag, fl_code, msg_str, msg_str2, q1_list_data, lvcarea, bill_date, res_bemerk, loopk, htparam, bill, res_line, queasy, guest
        nonlocal pvilanguage, dept, zinr, h_resnr, h_reslinnr, balance
        nonlocal guest2, bbuff


        nonlocal q1_list, guest2, bbuff
        nonlocal q1_list_data

        return {"dept_mbar": dept_mbar, "dept_ldry": dept_ldry, "bilrecid": bilrecid, "mc_pos1": mc_pos1, "mc_pos2": mc_pos2, "mc_flag": mc_flag, "fl_code": fl_code, "msg_str": msg_str, "msg_str2": msg_str2, "q1-list": q1_list_data}

    def check_creditlimit():

        nonlocal dept_mbar, dept_ldry, bilrecid, mc_pos1, mc_pos2, mc_flag, fl_code, msg_str, msg_str2, q1_list_data, lvcarea, bill_date, res_bemerk, loopk, htparam, bill, res_line, queasy, guest
        nonlocal pvilanguage, dept, zinr, h_resnr, h_reslinnr, balance
        nonlocal guest2, bbuff


        nonlocal q1_list, guest2, bbuff
        nonlocal q1_list_data

        klimit:Decimal = to_decimal("0.0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 68)]})

        guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

        if guest.kreditlimit != 0:
            klimit =  to_decimal(guest.kreditlimit)
        else:

            if htparam.fdecimal != 0:
                klimit =  to_decimal(htparam.fdecimal)
            else:
                klimit =  to_decimal(htparam.finteger)

        if (bill.saldo + balance) > klimit:
            msg_str2 = msg_str2 + chr_unicode(2) + "&Q" + translateExtended ("OVER Credit Limit found: ", lvcarea, "") + translateExtended ("Given Limit =", lvcarea, "") + " " + trim(to_string(klimit, ">>>,>>>,>>>,>>9")) + " / " + translateExtended ("Bill balance =", lvcarea, "") + " " + trim(to_string(bill.saldo, "->>>,>>>,>>>,>>9.99")) + chr_unicode(10) + translateExtended ("Restaurant balance =", lvcarea, "") + " " + trim(to_string(balance, "->>>,>>>,>>>,>>9.99")) + chr_unicode(10) + translateExtended ("Do you wish to CANCEL the room transfer?", lvcarea, "")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 949)]})

    if htparam.feldtyp == 1:
        dept_mbar = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})

    if htparam.feldtyp == 1:
        dept_ldry = htparam.finteger

    bill = get_cache (Bill, {"resnr": [(eq, h_resnr)],"reslinnr": [(eq, h_reslinnr)],"zinr": [(ne, "")],"flag": [(eq, 0)]})

    if bill:

        res_line = get_cache (Res_line, {"resnr": [(eq, h_resnr)],"reslinnr": [(eq, h_reslinnr)]})

        if res_line and res_line.code != "":

            queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

            if queasy and queasy.logi1 and dept != dept_mbar and dept != dept_ldry:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("CASH BASIS Billing Instruction :", lvcarea, "") + queasy.char1 + chr_unicode(10) + translateExtended ("Room Transfer not possible", lvcarea, "")
                bilrecid = 0
                fl_code = 1

                return generate_output()

        if bill.flag == 0:
            bilrecid = bill._recid
            check_creditlimit()
            fl_code = -1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 336)]})

    if htparam.feldtyp == 4:
        mc_flag = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 337)]})
        mc_pos1 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 338)]})
        mc_pos2 = htparam.finteger

    res_line_obj_list = {}
    res_line = Res_line()
    guest = Guest()
    bbuff = Bill()
    for res_line.code, res_line.resnr, res_line.zinr, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.bemerk, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line._recid, guest.kreditlimit, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.nation1, guest._recid, bbuff.gastnr, bbuff.saldo, bbuff._recid, bbuff.flag, bbuff.billnr, bbuff.name, bbuff.parent_nr in db_session.query(Res_line.code, Res_line.resnr, Res_line.zinr, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.bemerk, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line._recid, Guest.kreditlimit, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.nation1, Guest._recid, Bbuff.gastnr, Bbuff.saldo, Bbuff._recid, Bbuff.flag, Bbuff.billnr, Bbuff.name, Bbuff.parent_nr).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Bbuff,(Bbuff.resnr == Res_line.resnr) & (Bbuff.reslinnr == Res_line.reslinnr)).filter(
             (Res_line.active_flag == 1) & (Res_line.zinr >= (zinr).lower())).order_by(Res_line.zinr, Bbuff.parent_nr, Res_line.reslinnr, Res_line.name).all():
        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

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

                queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                if queasy and queasy.logi1:
                    q1_list.name_bg_col = 12
                    q1_list.name_fg_col = 15

        if res_line.resstatus == 12:
            q1_list.bill_bg_col = 2
            q1_list.bill_fg_col = 15


        q1_list.bemerk = replace_str(q1_list.bemerk, chr_unicode(10) , "")


        q1_list.bemerk = replace_str(q1_list.bemerk, chr_unicode(13) , "")
        q1_list.bemerk = replace_str(q1_list.bemerk, "~n", "")
        q1_list.bemerk = replace_str(q1_list.bemerk, "\\n", "")
        q1_list.bemerk = replace_str(q1_list.bemerk, "~r", "")
        q1_list.bemerk = replace_str(q1_list.bemerk, "~r~n", "")
        q1_list.bemerk = replace_str(q1_list.bemerk, chr_unicode(10) + chr_unicode(13) , "")
        res_bemerk = ""
        for loopk in range(1,length(q1_list.bemerk)  + 1) :

            if asc(substring(q1_list.bemerk, loopk - 1, 1)) == 0:
                pass
            else:
                res_bemerk = res_bemerk + substring(q1_list.bemerk, loopk - 1, 1)
        q1_list.bemerk = res_bemerk

        if length(q1_list.bemerk) < 3:
            q1_list.bemerk = replace_str(q1_list.bemerk, chr_unicode(32) , "")

        if length(q1_list.bemerk) == None:
            q1_list.bemerk = ""

    htparam = get_cache (Htparam, {"paramnr": [(eq, 974)]})

    if not htparam.flogical:

        return generate_output()
    bill_date = get_output(htpdate(110))

    res_line_obj_list = {}
    res_line = Res_line()
    guest = Guest()
    for res_line.code, res_line.resnr, res_line.zinr, res_line.resstatus, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.bemerk, res_line.ankunft, res_line.abreise, res_line.reslinnr, res_line.name, res_line._recid, guest.kreditlimit, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.nation1, guest._recid in db_session.query(Res_line.code, Res_line.resnr, Res_line.zinr, Res_line.resstatus, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.bemerk, Res_line.ankunft, Res_line.abreise, Res_line.reslinnr, Res_line.name, Res_line._recid, Guest.kreditlimit, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.nation1, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
             (Res_line.resstatus == 8) & (Res_line.abreise == bill_date) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zinr >= (zinr).lower())).order_by(Res_line.zinr, Res_line.reslinnr, Res_line.name).all():
        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True

        for bbuff in db_session.query(Bbuff).filter(
                 (Bbuff.resnr == res_line.resnr) & (Bbuff.parent_nr == res_line.reslinnr) & (Bbuff.saldo != 0)).order_by(Bbuff.reslinnr).all():
            q1_list = Q1_list()
            q1_list_data.append(q1_list)

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

                    queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                    if queasy and queasy.logi1:
                        q1_list.name_bg_col = 12
                        q1_list.name_fg_col = 15


            q1_list.bemerk = replace_str(q1_list.bemerk, chr_unicode(10) , "")


            q1_list.bemerk = replace_str(q1_list.bemerk, chr_unicode(13) , "")
            q1_list.bemerk = replace_str(q1_list.bemerk, "~n", "")
            q1_list.bemerk = replace_str(q1_list.bemerk, "\\n", "")
            q1_list.bemerk = replace_str(q1_list.bemerk, "~r", "")
            q1_list.bemerk = replace_str(q1_list.bemerk, "~r~n", "")
            q1_list.bemerk = replace_str(q1_list.bemerk, chr_unicode(10) + chr_unicode(13) , "")
            res_bemerk = ""
            for loopk in range(1,length(q1_list.bemerk)  + 1) :

                if asc(substring(q1_list.bemerk, loopk - 1, 1)) == 0:
                    pass
                else:
                    res_bemerk = res_bemerk + substring(q1_list.bemerk, loopk - 1, 1)
            q1_list.bemerk = res_bemerk

            if length(q1_list.bemerk) < 3:
                q1_list.bemerk = replace_str(q1_list.bemerk, chr_unicode(32) , "")

            if length(q1_list.bemerk) == None:
                q1_list.bemerk = ""

    return generate_output()