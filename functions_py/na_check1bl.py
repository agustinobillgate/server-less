#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 20/10/2025
# nama var: argt_betrag, sama dengan fungsi di functions_py/argt_betrag.py
# Rd 05/11/2025, nation -> getcache diganti query langsung karena ada masalah strip()
# Rd 05/11/2025, arrangement -> getcache diganti query langsung karena ada masalah strip()
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.argt_betrag import argt_betrag
from models import Res_line, Htparam, Bill, Guest, Nation, H_bill, Waehrung, Arrangement, Artikel, Argt_line, Reslin_queasy, Nightaudit

def na_check1bl(pvilanguage:int, def_natcode:string):

    prepare_cache ([Res_line, Htparam, Bill, Guest, H_bill, Waehrung, Arrangement, Artikel, Argt_line, Reslin_queasy, Nightaudit])

    msg_str = ""
    msg_str2 = ""
    msg_str3 = ""
    w_flag = False
    names_ok = False
    its_ok = False
    htparam_recid = 0
    lvcarea:string = "na-start"
    localregion_exist:bool = False
    sharerok:bool = True
    rmno:string = ""
    cidate:date = None
    billdate:date = None
    frate:Decimal = 1
    lodg_betrag:Decimal = to_decimal("0.0")
    # nama var: argt_betrag, sama dengan fungsi di functions_py/argt_betrag.py
    # argt_betrag:Decimal = to_decimal("0.0")
    var_argt_betrag:Decimal = to_decimal("0.0")
    ex_rate:Decimal = to_decimal("0.0")
    vat_art:Decimal = to_decimal("0.0")
    service_art:Decimal = to_decimal("0.0")
    vat2_art:Decimal = to_decimal("0.0")
    fact_art:Decimal = to_decimal("0.0")
    gross_argt:Decimal = to_decimal("0.0")
    net_argt:Decimal = to_decimal("0.0")
    bfast_value:Decimal = to_decimal("0.0")
    lunch_value:Decimal = to_decimal("0.0")
    dinner_value:Decimal = to_decimal("0.0")
    luncdin_value:Decimal = to_decimal("0.0")
    other_value:Decimal = to_decimal("0.0")
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    segment_type:int = 0
    passfirst:bool = False
    tmpdate:date = None
    na_date:date = None
    na_time:int = 0
    na_name:string = ""
    res_line = htparam = bill = guest = nation = h_bill = waehrung = arrangement = artikel = argt_line = reslin_queasy = nightaudit = None

    rbuff = None

    Rbuff = create_buffer("Rbuff",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, msg_str3, w_flag, names_ok, its_ok, htparam_recid, lvcarea, localregion_exist, sharerok, rmno, cidate, billdate, frate, lodg_betrag, var_argt_betrag, ex_rate, vat_art, service_art, vat2_art, fact_art, gross_argt, net_argt, bfast_value, lunch_value, dinner_value, luncdin_value, other_value, bfast_art, lunch_art, dinner_art, lundin_art, segment_type, passfirst, tmpdate, na_date, na_time, na_name, res_line, htparam, bill, guest, nation, h_bill, waehrung, arrangement, artikel, argt_line, reslin_queasy, nightaudit
        nonlocal pvilanguage, def_natcode
        nonlocal rbuff


        nonlocal rbuff

        return {"msg_str": msg_str, "msg_str2": msg_str2, "msg_str3": msg_str3, "w_flag": w_flag, "names_ok": names_ok, "its_ok": its_ok, "htparam_recid": htparam_recid}

    # def check_na_program_names():

    #     nonlocal msg_str, msg_str2, msg_str3, w_flag, names_ok, its_ok, htparam_recid, lvcarea, localregion_exist, sharerok, rmno, cidate, billdate, frate, lodg_betrag, var_argt_betrag, ex_rate, vat_art, service_art, vat2_art, fact_art, gross_argt, net_argt, bfast_value, lunch_value, dinner_value, luncdin_value, other_value, bfast_art, lunch_art, dinner_art, lundin_art, segment_type, passfirst, tmpdate, na_date, na_time, na_name, res_line, htparam, bill, guest, nation, h_bill, waehrung, arrangement, artikel, argt_line, reslin_queasy, nightaudit
    #     nonlocal pvilanguage, def_natcode
    #     nonlocal rbuff


    #     nonlocal rbuff

    #     names_ok = True
    #     progname:string = ""
    #     not_found:bool = False

    #     def generate_inner_output():
    #         return (names_ok)


    #     for nightaudit in db_session.query(Nightaudit).filter(
    #              (Nightaudit.selektion)).order_by((1 - Nightaudit.hogarest), Nightaudit.reihenfolge).all():
    #         progname = nightaudit.programm
    #         progname = ass_progname(nightaudit.abschlussart, progname)
    #         not_found = SEARCH (progname) == None

    #         if not_found:
    #             progname = replace_str(progname, ".p", ".r")
    #             progname = replace_str(progname, ".w", ".r")
    #             not_found = (SEARCH (progname) == None)

    #         if not_found:

    #             if matches(progname,r"nt-tauziarpt.r") or matches(progname,r"nt-exportgcf.r") or matches(progname,r"nt-exportghs.r") or matches(progname,r"nt-exportghs2.r") or matches(progname,r"nt-salesboard.r") or matches(progname,r"nt-dashboardohm-daily.r") or matches(progname,r"nt-dashboard-daily.r") or matches(progname,r"nt-exportguestsense.r") or matches(progname,r"nt-exportghs-phm.r") or matches(progname,r"nt-guestlist-csv.r"):
    #                 pass
    #             else:
    #                 msg_str = msg_str + chr_unicode(2) + translateExtended ("N/a Program does not exist:", lvcarea, "") + " " + nightaudit.program
    #                 names_ok = False

    #                 return generate_inner_output()

    #     return generate_inner_output()


    # def ass_progname(abschlussart:int, progname:string):

    #     nonlocal msg_str, msg_str2, msg_str3, w_flag, names_ok, its_ok, htparam_recid, lvcarea, localregion_exist, sharerok, rmno, cidate, billdate, frate, lodg_betrag, var_argt_betrag, ex_rate, vat_art, service_art, vat2_art, fact_art, gross_argt, net_argt, bfast_value, lunch_value, dinner_value, luncdin_value, other_value, bfast_art, lunch_art, dinner_art, lundin_art, segment_type, passfirst, tmpdate, na_date, na_time, na_name, res_line, htparam, bill, guest, nation, h_bill, waehrung, arrangement, artikel, argt_line, reslin_queasy, nightaudit
    #     nonlocal pvilanguage, def_natcode
    #     nonlocal rbuff


    #     nonlocal rbuff

    #     a:int = 0

    #     def generate_inner_output():
    #         return (progname)


    #     if matches(progname,r"*bl.p*"):
    #         pass
    #     else:

    #         if to_int(abschlussart) == 1:
    #             pass
    #         else:
    #             a = R_INDEX (progname, ".p")
    #             progname = substring(progname , 0, a - 1) + "bl.p"

    #     return generate_inner_output()


    cidate = get_output(htpdate(87))
    billdate = get_output(htpdate(110))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})
    bfast_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})
    lunch_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})
    dinner_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 229)]})
    lundin_art = htparam.finteger

    if billdate != cidate:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Wrong Check-in date or Billing date (must be equal).", lvcarea, "")

        return generate_output()

    if billdate >= get_current_date():
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Night-Audit not possible (too early).", lvcarea, "")

        return generate_output()

    for res_line in db_session.query(Res_line).filter(
             (Res_line.resstatus == 8) & (Res_line.abreise == billdate) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

        bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"parent_nr": [(eq, res_line.reslinnr)],"saldo": [(ne, 0)]})

        if bill:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Night-Audit not possible:", lvcarea, "") + chr_unicode(10) + translateExtended ("Unbalanced bill of checked-out guest exists", lvcarea, "")

            return generate_output()

    for res_line in db_session.query(Res_line).filter(
             (Res_line.active_flag == 1) & (Res_line.resstatus == 13) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).yield_per(100):

        rbuff = get_cache (Res_line, {"active_flag": [(eq, 1)],"resstatus": [(eq, 6)],"zinr": [(eq, res_line.zinr)]})

        if not rbuff:
            rmno = res_line.zinr
            sharerok = False


            break

    if not sharerok:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Room Sharer found with no main guest: rmno", lvcarea, "") + " " + rmno

        return generate_output()

    for res_line in db_session.query(Res_line).filter(
             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).yield_per(100):

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if not guest:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Guest record of inhouse guest not found: rmno", lvcarea, "") + " " + res_line.zinr + chr_unicode(10) + translateExtended ("Night-Audit not possible.", lvcarea, "")

            return generate_output()

        # nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1.strip())]})
        nation = db_session.query(Nation).filter(
                 (Nation.kurzbez == guest.nation1.strip())).first()

        if not nation:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Nationality of inhouse guest not defined: rmno", lvcarea, "") + " " + res_line.zinr + chr_unicode(10) + translateExtended ("Night-Audit not possible.", lvcarea, "")

            return generate_output()

    res_line = db_session.query(Res_line).filter(
             (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.abreise == billdate)).first()

    if res_line:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Today departing inhouse guest(s) found: rmno", lvcarea, "") + " " + res_line.zinr + chr_unicode(10) + translateExtended ("Night-Audit not possible.", lvcarea, "")

        return generate_output()

    h_bill = get_cache (H_bill, {"flag": [(eq, 0)],"rechnr": [(gt, 0)]})

    if h_bill:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("N/a not possible as opened Restaurant bill(s) found :", lvcarea, "") + chr_unicode(10) + translateExtended ("Department", lvcarea, "") + " " + to_string(h_bill.departement) + " " + translateExtended ("BillNo", lvcarea, "") + " " + to_string(h_bill.rechnr)

        return generate_output()

    nation = get_cache (Nation, {"natcode": [(gt, 0)]})
    localregion_exist = None != nation

    for res_line in db_session.query(Res_line).filter(
             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).yield_per(100):

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

        if not waehrung:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Currency not found for the following reservation :", lvcarea, "") + chr_unicode(10) + translateExtended ("ResNo :", lvcarea, "") + " " + to_string(res_line.resnr) + " - " + res_line.zinr + " " + res_line.name
            w_flag = True
        else:

            if waehrung.ankauf == 0 or waehrung.einheit == 0:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Currency Rate incorrect for the following reservation :", lvcarea, "") + chr_unicode(10) + translateExtended ("Code :", lvcarea, "") + " " + waehrung.wabkurz + " - " + res_line.zinr + " " + res_line.name
                w_flag = True

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if not guest:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Guest record not found for following reservation :", lvcarea, "") + chr_unicode(10) + res_line.zinr + " " + res_line.name
            w_flag = True
            break
        else:

            # nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})
            nation = db_session.query(Nation).filter(
                     (Nation.kurzbez == guest.nation1.strip())).first()

            if not nation:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Nation code not correctly defined for following reservation :", lvcarea, "") + chr_unicode(10) + res_line.zinr + " " + res_line.name
                w_flag = True
                break

            # nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})
            nation = db_session.query(Nation).filter(
                     (Nation.kurzbez == guest.land.strip())).first()

            if not nation:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Country code not correctly defined for following reservation :", lvcarea, "") + chr_unicode(10) + res_line.zinr + " " + res_line.name
                w_flag = True
                break

            if localregion_exist and (guest.land  == (def_natcode)):

                # nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation2)],"natcode": [(gt, 0)]})
                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == guest.nation2.strip()) & (Nation.natcode > 0)).first()

                if not nation:
                    msg_str = msg_str + chr_unicode(2) + translateExtended ("Local Region code not correctly defined for following reservation :", lvcarea, "") + chr_unicode(10) + res_line.zinr + " " + res_line.name
                    w_flag = True
                    break

            if guest.land  == ("UNK") :
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Country code UNK found for following reservation :", lvcarea, "") + chr_unicode(10) + res_line.zinr + " " + res_line.name + chr_unicode(10) + "Please change another code"
                w_flag = True
                break

            elif guest.nation1  == ("UNK") :
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Nation code UNK found for following reservation :", lvcarea, "") + chr_unicode(10) + res_line.zinr + " " + res_line.name + chr_unicode(10) + "Please change another code"
                w_flag = True
                break

        if res_line.zipreis != 0:

            if res_line.reserve_dec != 0:
                frate =  to_decimal(res_line.reserve_dec)
            else:

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            lodg_betrag =  to_decimal("0")
            lodg_betrag =  to_decimal(res_line.zipreis) * to_decimal(frate)

            # arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == res_line.arrangement.strip())).first()

            argt_line_obj_list = {}
            argt_line = Argt_line()
            artikel = Artikel()
            for argt_line._recid, artikel.umsatzart, artikel.zwkum, artikel._recid in db_session.query(Argt_line._recid, Artikel.umsatzart, Artikel.zwkum, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                     (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
                if argt_line_obj_list.get(argt_line._recid):
                    continue
                else:
                    argt_line_obj_list[argt_line._recid] = True


                var_argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))

                if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(var_argt_betrag)

                elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(var_argt_betrag)

                elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(var_argt_betrag)

                elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(var_argt_betrag)
                else:
                    lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(var_argt_betrag)

            if lodg_betrag < 0:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Minus lodging found with reservation : ", lvcarea, "") + to_string(res_line.resnr) + "/" + to_string(res_line.reslinnr, "999")
                w_flag = True
                break
        passfirst = True

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("arrangement")) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy.date1).yield_per(100):

            if passfirst == False:

                if tmpdate >= reslin_queasy.date1:
                    msg_str = msg_str + chr_unicode(2) + translateExtended ("overlapping fixed rate", lvcarea, "") + chr_unicode(10) + translateExtended ("please check fixed rate in reservation: ", lvcarea, "") + to_string(reslin_queasy.resnr)
                    w_flag = True
                    break
            passfirst = False
            tmpdate = reslin_queasy.date2

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, cidate)],"date2": [(ge, cidate)],"char1": [(ne, "")]})

        if reslin_queasy and res_line.arrangement != reslin_queasy.char1:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Different Arrangement Code between reservation and fixed rate.", lvcarea, "") + chr_unicode(10) + translateExtended ("Night Audit process not possible. Please check it.", lvcarea, "")
            w_flag = True
            break

        if w_flag:
            break

    if w_flag :

        return generate_output()
    
    # Rd, 20/10/2025: comment karena fungsi check_na_program_names belum diimplementasi
    # names_ok = check_na_program_names()
    names_ok = True


    if not names_ok:

        return generate_output()

    bill = db_session.query(Bill).filter(
             (Bill.flag == 1) & ((Bill.saldo >= 0.1) | (Bill.saldo <= -0.1))).first()

    if bill:
        msg_str2 = msg_str2 + chr_unicode(2) + "&W" + translateExtended ("Closed bill with a non zero balance found: BillNo =", lvcarea, "") + " " + trim(to_string(bill.rechnr, ">>>,>>>,>>9")) + " - " + to_string(bill.saldo)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

    if not htparam.flogical:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 102)]})
        na_date = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 103)]})
        na_time = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})
        na_name = htparam.fchar

        if na_date == get_current_date():
            msg_str3 = msg_str3 + chr_unicode(2) + "&W" + translateExtended ("The last night audit was running TODAY", lvcarea, "") + chr_unicode(10) + to_string(na_date) + " " + translateExtended ("at", lvcarea, "") + " " + to_string(na_time, "HH:MM") + " " + translateExtended ("by", lvcarea, "") + " " + na_name
        its_ok = True
    else:
        msg_str3 = msg_str3 + chr_unicode(2) + translateExtended ("Night audit flag is active!", lvcarea, "")

    if its_ok:
        pass
        htparam_recid = htparam._recid

    return generate_output()