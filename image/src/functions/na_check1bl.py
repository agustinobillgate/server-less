from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.argt_betrag import argt_betrag
from sqlalchemy import func
import re
from models import Res_line, Htparam, Bill, Guest, Nation, H_bill, Waehrung, Arrangement, Artikel, Argt_line, Reslin_queasy, Nightaudit

def na_check1bl(pvilanguage:int, def_natcode:str):
    msg_str = ""
    msg_str2 = ""
    msg_str3 = ""
    w_flag = False
    names_ok = False
    its_ok = False
    htparam_recid = 0
    lvcarea:str = "na_start"
    localregion_exist:bool = False
    sharerok:bool = True
    rmno:str = ""
    cidate:date = None
    billdate:date = None
    frate:decimal = 1
    lodg_betrag:decimal = 0
    argt_betrag:decimal = 0
    ex_rate:decimal = 0
    vat_art:decimal = 0
    service_art:decimal = 0
    vat2_art:decimal = 0
    fact_art:decimal = 0
    gross_argt:decimal = 0
    net_argt:decimal = 0
    bfast_value:decimal = 0
    lunch_value:decimal = 0
    dinner_value:decimal = 0
    luncdin_value:decimal = 0
    other_value:decimal = 0
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    segment_type:int = 0
    passfirst:bool = False
    tmpdate:date = None
    na_date:date = None
    na_time:int = 0
    na_name:str = ""
    res_line = htparam = bill = guest = nation = h_bill = waehrung = arrangement = artikel = argt_line = reslin_queasy = nightaudit = None

    rbuff = None

    Rbuff = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, msg_str3, w_flag, names_ok, its_ok, htparam_recid, lvcarea, localregion_exist, sharerok, rmno, cidate, billdate, frate, lodg_betrag, argt_betrag, ex_rate, vat_art, service_art, vat2_art, fact_art, gross_argt, net_argt, bfast_value, lunch_value, dinner_value, luncdin_value, other_value, bfast_art, lunch_art, dinner_art, lundin_art, segment_type, passfirst, tmpdate, na_date, na_time, na_name, res_line, htparam, bill, guest, nation, h_bill, waehrung, arrangement, artikel, argt_line, reslin_queasy, nightaudit
        nonlocal rbuff


        nonlocal rbuff
        return {"msg_str": msg_str, "msg_str2": msg_str2, "msg_str3": msg_str3, "w_flag": w_flag, "names_ok": names_ok, "its_ok": its_ok, "htparam_recid": htparam_recid}

    def check_na_program_names():

        nonlocal msg_str, msg_str2, msg_str3, w_flag, names_ok, its_ok, htparam_recid, lvcarea, localregion_exist, sharerok, rmno, cidate, billdate, frate, lodg_betrag, argt_betrag, ex_rate, vat_art, service_art, vat2_art, fact_art, gross_argt, net_argt, bfast_value, lunch_value, dinner_value, luncdin_value, other_value, bfast_art, lunch_art, dinner_art, lundin_art, segment_type, passfirst, tmpdate, na_date, na_time, na_name, res_line, htparam, bill, guest, nation, h_bill, waehrung, arrangement, artikel, argt_line, reslin_queasy, nightaudit
        nonlocal rbuff


        nonlocal rbuff

        names_ok = False
        progname:str = ""
        not_found:bool = False

        def generate_inner_output():
            return names_ok

        for nightaudit in db_session.query(Nightaudit).filter(
                (Nightaudit.selektion)).all():
            progname = nightaudit.programm
            progname = ass_progname(nightaudit.abschlussart, progname)
            not_found = SEARCH (progname.lower()) == None

            if not_found:
                progname = replace_str(progname, ".p", ".r")
                progname = replace_str(progname, ".w", ".r")
                not_found = (SEARCH (progname.lower()) == None)

            if not_found:

                if re.match("nt_tauziarpt.r",progname) or re.match("nt_exportgcf.r",progname) or re.match("nt_exportghs.r",progname) or re.match("nt_salesboard.r",progname) or re.match("nt_dashboardohm_daily.r",progname) or re.match("nt_dashboard_daily.r",progname):
                    pass
                else:
                    msg_str = msg_str + chr(2) + translateExtended ("N/a Program does not exist:", lvcarea, "") + " " + nightaudit.program
                    names_ok = False

                    return generate_inner_output()


        return generate_inner_output()

    def ass_progname(abschlussart:int, progname:str):

        nonlocal msg_str, msg_str2, msg_str3, w_flag, names_ok, its_ok, htparam_recid, lvcarea, localregion_exist, sharerok, rmno, cidate, billdate, frate, lodg_betrag, argt_betrag, ex_rate, vat_art, service_art, vat2_art, fact_art, gross_argt, net_argt, bfast_value, lunch_value, dinner_value, luncdin_value, other_value, bfast_art, lunch_art, dinner_art, lundin_art, segment_type, passfirst, tmpdate, na_date, na_time, na_name, res_line, htparam, bill, guest, nation, h_bill, waehrung, arrangement, artikel, argt_line, reslin_queasy, nightaudit
        nonlocal rbuff


        nonlocal rbuff

        a:int = 0

        if re.match(".*bl.p.*",progname):
            1
        else:

            if to_int(abschlussart) == 1:
                pass
            else:
                a = R_INDEX (progname, ".p")
                progname = substring(progname.lower() , 0, a - 1) + "bl.p"

    cidate = get_output(htpdate(87))
    billdate = get_output(htpdate(110))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 125)).first()
    bfast_art = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 227)).first()
    lunch_art = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 228)).first()
    dinner_art = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 229)).first()
    lundin_art = finteger

    if billdate != cidate:
        msg_str = msg_str + chr(2) + translateExtended ("Wrong Check_in date or Billing date (must be equal).", lvcarea, "")

        return generate_output()

    if billdate >= get_current_date():
        msg_str = msg_str + chr(2) + translateExtended ("Night_Audit not possible (too early).", lvcarea, "")

        return generate_output()

    for res_line in db_session.query(Res_line).filter(
            (Res_line.resstatus == 8) &  (Res_line.abreise == billdate) &  (Res_line.l_zuordnung[2] == 0)).all():

        bill = db_session.query(Bill).filter(
                (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.saldo != 0)).first()

        if bill:
            msg_str = msg_str + chr(2) + translateExtended ("Night_Audit not possible:", lvcarea, "") + chr(10) + translateExtended ("Unbalanced bill of checked_out guest exists", lvcarea, "")

            return generate_output()

    for res_line in db_session.query(Res_line).filter(
            (Res_line.active_flag == 1) &  (Res_line.resstatus == 13) &  (Res_line.l_zuordnung[2] == 0)).all():

        rbuff = db_session.query(Rbuff).filter(
                (Rbuff.active_flag == 1) &  (Rbuff.resstatus == 6) &  (Rbuff.zinr == res_line.zinr)).first()

        if not rbuff:
            rmno = res_line.zinr
            sharerok = False


            break

    if not sharerok:
        msg_str = msg_str + chr(2) + translateExtended ("Room Sharer found with no main guest: rmno", lvcarea, "") + " " + rmno

        return generate_output()

    for res_line in db_session.query(Res_line).filter(
            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.l_zuordnung[2] == 0)).all():

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()

        if not guest:
            msg_str = msg_str + chr(2) + translateExtended ("Guest record of inhouse guest not found: rmno", lvcarea, "") + " " + res_line.zinr + chr(10) + translateExtended ("Night_Audit not possible.", lvcarea, "")

            return generate_output()

        nation = db_session.query(Nation).filter(
                (Nation.kurzbez == guest.nation1)).first()

        if not nation:
            msg_str = msg_str + chr(2) + translateExtended ("Nationality of inhouse guest not defined: rmno", lvcarea, "") + " " + res_line.zinr + chr(10) + translateExtended ("Night_Audit not possible.", lvcarea, "")

            return generate_output()

    res_line = db_session.query(Res_line).filter(
            (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.abreise == billdate)).first()

    if res_line:
        msg_str = msg_str + chr(2) + translateExtended ("Today departing inhouse guest(s) found: rmno", lvcarea, "") + " " + res_line.zinr + chr(10) + translateExtended ("Night_Audit not possible.", lvcarea, "")

        return generate_output()

    h_bill = db_session.query(H_bill).filter(
                (H_bill.flag == 0) &  (H_bill.rechnr > 0)).first()

    if h_bill:
        msg_str = msg_str + chr(2) + translateExtended ("N/a not possible as opened Restaurant bill(s) found :", lvcarea, "") + chr(10) + translateExtended ("Department", lvcarea, "") + " " + to_string(h_bill.departement) + " " + translateExtended ("BillNo", lvcarea, "") + " " + to_string(h_bill.rechnr)

        return generate_output()

    nation = db_session.query(Nation).filter(
            (Nation.natcode > 0)).first()
    localregion_exist = None != nation

    for res_line in db_session.query(Res_line).filter(
            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.l_zuordnung[2] == 0)).all():

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == res_line.betriebsnr)).first()

        if not waehrung:
            msg_str = msg_str + chr(2) + translateExtended ("Currency not found for the following reservation :", lvcarea, "") + chr(10) + translateExtended ("ResNo :", lvcarea, "") + " " + to_string(res_line.resnr) + " - " + res_line.zinr + " " + res_line.name
            w_flag = True
        else:

            if waehrung.ankauf == 0 or waehrung.einheit == 0:
                msg_str = msg_str + chr(2) + translateExtended ("Currency Rate incorrect for the following reservation :", lvcarea, "") + chr(10) + translateExtended ("Code :", lvcarea, "") + " " + waehrung.wabkurz + " - " + res_line.zinr + " " + res_line.name
                w_flag = True

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()

        if not guest:
            msg_str = msg_str + chr(2) + translateExtended ("Guest record not found for following reservation :", lvcarea, "") + chr(10) + res_line.zinr + " " + res_line.name
            w_flag = True
            break
        else:

            nation = db_session.query(Nation).filter(
                    (Nation.kurzbez == guest.nation1)).first()

            if not nation:
                msg_str = msg_str + chr(2) + translateExtended ("Nation code not correctly defined for following reservation :", lvcarea, "") + chr(10) + res_line.zinr + " " + res_line.name
                w_flag = True
                break

            nation = db_session.query(Nation).filter(
                    (Nation.kurzbez == guest.land)).first()

            if not nation:
                msg_str = msg_str + chr(2) + translateExtended ("Country code not correctly defined for following reservation :", lvcarea, "") + chr(10) + res_line.zinr + " " + res_line.name
                w_flag = True
                break

            if localregion_exist and (guest.land == def_natcode):

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == guest.nation2) &  (Nation.natcode > 0)).first()

                if not nation:
                    msg_str = msg_str + chr(2) + translateExtended ("Local Region code not correctly defined for following reservation :", lvcarea, "") + chr(10) + res_line.zinr + " " + res_line.name
                    w_flag = True
                    break

            if guest.land.lower()  == "UNK":
                msg_str = msg_str + chr(2) + translateExtended ("Country code UNK found for following reservation :", lvcarea, "") + chr(10) + res_line.zinr + " " + res_line.name + chr(10) + "Please change another code"
                w_flag = True
                break

            elif guest.nation1.lower()  == "UNK":
                msg_str = msg_str + chr(2) + translateExtended ("Nation code UNK found for following reservation :", lvcarea, "") + chr(10) + res_line.zinr + " " + res_line.name + chr(10) + "Please change another code"
                w_flag = True
                break

        if res_line.zipreis != 0:

            if res_line.reserve_dec != 0:
                frate = res_line.reserve_dec
            else:

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    frate = waehrung.ankauf / waehrung.einheit
            lodg_betrag = 0
            lodg_betrag = res_line.zipreis * frate

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement == res_line.arrangement)).first()

            argt_line_obj_list = []
            for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) &  (Artikel.departement == Argt_line.departement)).filter(
                    (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2) &  (Argt_line.kind1)).all():
                if argt_line._recid in argt_line_obj_list:
                    continue
                else:
                    argt_line_obj_list.append(argt_line._recid)


                argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))

                if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    lodg_betrag = lodg_betrag - argt_betrag

                elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    lodg_betrag = lodg_betrag - argt_betrag

                elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    lodg_betrag = lodg_betrag - argt_betrag

                elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    lodg_betrag = lodg_betrag - argt_betrag
                else:
                    lodg_betrag = lodg_betrag - argt_betrag

            if lodg_betrag < 0:
                msg_str = msg_str + chr(2) + translateExtended ("Minus lodging found with reservation : ", lvcarea, "") + to_string(res_line.resnr) + "/" + to_string(res_line.reslinnr, "999")
                w_flag = True
                break
        passfirst = True

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():

            if passfirst == False:

                if tmpdate >= reslin_queasy.date1:
                    msg_str = msg_str + chr(2) + translateExtended ("overlapping fixed rate", lvcarea, "") + chr (10) + translateExtended ("please check fixed rate in reservation: ", lvcarea, "") + to_string(reslin_queasy.resnr)
                    w_flag = True
                    break
            passfirst = False
            tmpdate = reslin_queasy.date2

        if w_flag:
            break

    if w_flag :

        return generate_output()
    names_ok = check_na_program_names()

    if not names_ok:

        return generate_output()

    bill = db_session.query(Bill).filter(
            (Bill.flag == 1) &  ((Bill.saldo >= 0.1) |  (Bill.saldo <= -0.1))).first()

    if bill:
        msg_str2 = msg_str2 + chr(2) + "&W" + translateExtended ("Closed bill with a non zero balance found: BillNo  == ", lvcarea, "") + " " + trim(to_string(bill.rechnr, ">>>,>>>,>>9")) + " - " + to_string(bill.saldo)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 253)).first()

    if not htparam.flogical:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 102)).first()
        na_date = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 103)).first()
        na_time = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 253)).first()
        na_name = htparam.fchar

        if na_date == get_current_date():
            msg_str3 = msg_str3 + chr(2) + "&W" + translateExtended ("The last night audit was running TODAY", lvcarea, "") + chr(10) + to_string(na_date) + " " + translateExtended ("at", lvcarea, "") + " " + to_string(na_time, "HH:MM") + "  " + translateExtended ("by", lvcarea, "") + " " + na_name
        its_ok = True
    else:
        msg_str3 = msg_str3 + chr(2) + translateExtended ("Night audit flag is active!", lvcarea, "")

    if its_ok:

        htparam = db_session.query(Htparam).first()
        htparam_recid = htparam._recid

    return generate_output()