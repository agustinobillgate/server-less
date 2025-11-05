#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 05/11/2025
# 
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Res_line, Guest, Htparam, Queasy, Reslin_queasy, Reservation, Zimmer, Waehrung, Master, Counters, Guestseg

def fo_invoice_open_bill_cld_2bl(bil_flag:int, bil_recid:int, room:string, vipflag:bool):

    prepare_cache ([Bill, Res_line, Guest, Htparam, Queasy, Zimmer, Waehrung, Master, Counters])

    abreise = None
    resname = ""
    res_exrate = to_decimal("0.0")
    zimmer_bezeich = ""
    kreditlimit = to_decimal("0.0")
    master_str = ""
    master_rechnr = ""
    bill_anzahl = 0
    queasy_char1 = ""
    disp_warning = False
    flag_report = False
    guest_taxcode = ""
    repeat_charge = False
    t_res_line_data = []
    t_bill_data = []
    vipnr1:int = 99999
    vipnr2:int = 99999
    vipnr3:int = 99999
    vipnr4:int = 99999
    vipnr5:int = 99999
    vipnr6:int = 99999
    vipnr7:int = 99999
    vipnr8:int = 99999
    vipnr9:int = 99999
    ci_date:date = None
    g_address:string = ""
    g_wonhort:string = ""
    g_plz:string = ""
    g_land:string = ""
    bill = res_line = guest = htparam = queasy = reslin_queasy = reservation = zimmer = waehrung = master = counters = guestseg = None

    t_bill = t_res_line = resbuff = guestmember = mbill = bill1 = None

    t_bill_data, T_bill = create_model_like(Bill)
    t_res_line_data, T_res_line = create_model_like(Res_line, {"guest_name":string})

    Resbuff = create_buffer("Resbuff",Res_line)
    Guestmember = create_buffer("Guestmember",Guest)
    Mbill = create_buffer("Mbill",Bill)
    Bill1 = create_buffer("Bill1",Bill)


    db_session = local_storage.db_session
    room = room.strip()

    def generate_output():
        nonlocal abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, guest_taxcode, repeat_charge, t_res_line_data, t_bill_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ci_date, g_address, g_wonhort, g_plz, g_land, bill, res_line, guest, htparam, queasy, reslin_queasy, reservation, zimmer, waehrung, master, counters, guestseg
        nonlocal bil_flag, bil_recid, room, vipflag
        nonlocal resbuff, guestmember, mbill, bill1


        nonlocal t_bill, t_res_line, resbuff, guestmember, mbill, bill1
        nonlocal t_bill_data, t_res_line_data

        return {"abreise": abreise, "resname": resname, "res_exrate": res_exrate, "zimmer_bezeich": zimmer_bezeich, "kreditlimit": kreditlimit, "master_str": master_str, "master_rechnr": master_rechnr, "bill_anzahl": bill_anzahl, "queasy_char1": queasy_char1, "disp_warning": disp_warning, "flag_report": flag_report, "guest_taxcode": guest_taxcode, "repeat_charge": repeat_charge, "t-res-line": t_res_line_data, "t-bill": t_bill_data}

    def check_vip(gastnr:int):

        nonlocal abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, guest_taxcode, repeat_charge, t_res_line_data, t_bill_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ci_date, g_address, g_wonhort, g_plz, g_land, bill, res_line, guest, htparam, queasy, reslin_queasy, reservation, zimmer, waehrung, master, counters, guestseg
        nonlocal bil_flag, bil_recid, room, vipflag
        nonlocal resbuff, guestmember, mbill, bill1


        nonlocal t_bill, t_res_line, resbuff, guestmember, mbill, bill1
        nonlocal t_bill_data, t_res_line_data

        guestseg = get_cache (Guestseg, {"gastnr": [(eq, gastnr)]})
        while None != guestseg and not vipflag:

            if (guestseg.segmentcode == vipnr1 or guestseg.segmentcode == vipnr2 or guestseg.segmentcode == vipnr3 or guestseg.segmentcode == vipnr4 or guestseg.segmentcode == vipnr5 or guestseg.segmentcode == vipnr6 or guestseg.segmentcode == vipnr7 or guestseg.segmentcode == vipnr8 or guestseg.segmentcode == vipnr9):
                vipflag = True

            curr_recid = guestseg._recid
            guestseg = db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == gastnr) & (Guestseg._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

    if res_line:
        t_res_line = T_res_line()
        t_res_line_data.append(t_res_line)

        buffer_copy(res_line, t_res_line)

        guestmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guestmember:
            t_res_line.guest_name = guestmember.anrede1 + " " + guestmember.name + ", " + guestmember.vorname1
    t_bill = T_bill()
    t_bill_data.append(t_bill)

    buffer_copy(bill, t_bill)

    resbuff = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

    if resbuff:
        abreise = resbuff.abreise
    else:
        abreise = bill.datum

    queasy = get_cache (Queasy, {"key": [(eq, 301)],"number1": [(eq, res_line.resnr)],"logi1": [(eq, True)]})

    if queasy:
        repeat_charge = queasy.logi1

    if res_line and bil_flag == 0 and res_line.abreise == ci_date:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("flag")) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.betriebsnr == 0) & ((Reslin_queasy.logi1) | (Reslin_queasy.logi2) | (Reslin_queasy.logi3))).first()

        if reslin_queasy:
            flag_report = True

    reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})
    resname = ""

    guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
    g_address = guest.adresse1
    g_wonhort = guest.wohnort
    g_plz = guest.plz
    g_land = guest.land
    guest_taxcode = to_string(guest.firmen_nr)


    if g_address == None:
        g_address = ""

    if g_wonhort == None:
        g_wonhort = ""

    if g_plz == None:
        g_plz = ""

    if g_land == None:
        g_land = ""
    resname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1 + chr_unicode(10) + g_address + chr_unicode(10) + g_wonhort + " " + g_plz + chr_unicode(10) + g_land

    if guest.kreditlimit != 0:
        kreditlimit =  to_decimal(guest.kreditlimit)
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 68)]})

        if htparam.fdecimal != 0:
            kreditlimit =  to_decimal(htparam.fdecimal)
        else:
            kreditlimit =  to_decimal(htparam.finteger)

    zimmer = get_cache (Zimmer, {"zinr": [(eq, bill.zinr)]})
    zimmer_bezeich = zimmer.bezeich
    res_exrate =  to_decimal("1")

    if res_line:

        if res_line.reserve_dec != 0:
            res_exrate =  to_decimal(res_line.reserve_dec)
        else:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

            if waehrung:
                res_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger
    check_vip(bill.gastnr)

    if not vipflag and guestmember:
        check_vip(guestmember.gastnr)
    master_str = ""
    master_rechnr = ""

    master = get_cache (Master, {"resnr": [(eq, bill.resnr)]})

    if master:

        mbill = get_cache (Bill, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, 0)],"zinr": [(eq, "")]})

        if not mbill:

            counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
            counters.counter = counters.counter + 1
            pass
            mbill = Bill()
            db_session.add(mbill)

            mbill.rechnr = counters.counter
            pass
            pass
            master.rechnr = mbill.rechnr
            pass

        if mbill:
            master_str = "Master Bill"
            master_rechnr = to_string(mbill.rechnr) + " - " + mbill.name
    bill_anzahl = 0

    if bill.flag == 0:

        for bill1 in db_session.query(Bill1).filter(
                     (Bill1.resnr == bill.resnr) & (Bill1.parent_nr == bill.parent_nr) & (Bill1.parent_nr != 0) & (Bill1.flag == 0) & (Bill1.zinr == bill.zinr)).order_by(Bill1._recid).all():
            bill_anzahl = bill_anzahl + 1


    if res_line and res_line.code.strip() != "" and bill.flag == 0:

        # queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code.strip()))]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 9) & (Queasy.number1 == to_int(res_line.code.strip()))).first()

        if queasy and queasy.logi1:
            queasy_char1 = queasy.char1

    return generate_output()