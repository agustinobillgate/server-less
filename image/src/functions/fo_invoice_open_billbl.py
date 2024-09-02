from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bill, Res_line, Guest, Htparam, Reslin_queasy, Reservation, Zimmer, Waehrung, Master, Counters, Queasy, Guestseg

def fo_invoice_open_billbl(bil_flag:int, bil_recid:int, room:str, vipflag:bool):
    abreise = None
    resname = ""
    res_exrate = 0
    zimmer_bezeich = ""
    kreditlimit = 0
    master_str = ""
    master_rechnr = ""
    bill_anzahl = 0
    queasy_char1 = ""
    disp_warning = False
    flag_report = False
    t_res_line_list = []
    t_bill_list = []
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
    g_address:str = ""
    g_wonhort:str = ""
    g_plz:str = ""
    g_land:str = ""
    bill = res_line = guest = htparam = reslin_queasy = reservation = zimmer = waehrung = master = counters = queasy = guestseg = None

    t_bill = t_res_line = resbuff = guestmember = mbill = bill1 = None

    t_bill_list, T_bill = create_model_like(Bill)
    t_res_line_list, T_res_line = create_model_like(Res_line)

    Resbuff = Res_line
    Guestmember = Guest
    Mbill = Bill
    Bill1 = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, t_res_line_list, t_bill_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ci_date, g_address, g_wonhort, g_plz, g_land, bill, res_line, guest, htparam, reslin_queasy, reservation, zimmer, waehrung, master, counters, queasy, guestseg
        nonlocal resbuff, guestmember, mbill, bill1


        nonlocal t_bill, t_res_line, resbuff, guestmember, mbill, bill1
        nonlocal t_bill_list, t_res_line_list
        return {"abreise": abreise, "resname": resname, "res_exrate": res_exrate, "zimmer_bezeich": zimmer_bezeich, "kreditlimit": kreditlimit, "master_str": master_str, "master_rechnr": master_rechnr, "bill_anzahl": bill_anzahl, "queasy_char1": queasy_char1, "disp_warning": disp_warning, "flag_report": flag_report, "t-res-line": t_res_line_list, "t-bill": t_bill_list}

    def check_vip(gastnr:int):

        nonlocal abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, t_res_line_list, t_bill_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ci_date, g_address, g_wonhort, g_plz, g_land, bill, res_line, guest, htparam, reslin_queasy, reservation, zimmer, waehrung, master, counters, queasy, guestseg
        nonlocal resbuff, guestmember, mbill, bill1


        nonlocal t_bill, t_res_line, resbuff, guestmember, mbill, bill1
        nonlocal t_bill_list, t_res_line_list

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == gastnr)).first()
        while None != guestseg and not vipflag:

            if (guestseg.segmentcode == vipnr1 or guestseg.segmentcode == vipnr2 or guestseg.segmentcode == vipnr3 or guestseg.segmentcode == vipnr4 or guestseg.segmentcode == vipnr5 or guestseg.segmentcode == vipnr6 or guestseg.segmentcode == vipnr7 or guestseg.segmentcode == vipnr8 or guestseg.segmentcode == vipnr9):
                vipflag = True

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == gastnr)).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = fdate

    bill = db_session.query(Bill).filter(
            (Bill._recid == bil_recid)).first()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

    if res_line:
        t_res_line = T_res_line()
        t_res_line_list.append(t_res_line)

        buffer_copy(res_line, t_res_line)

        guestmember = db_session.query(Guestmember).filter(
                (Guestmember.gastnr == res_line.gastnrmember)).first()
    t_bill = T_bill()
    t_bill_list.append(t_bill)

    buffer_copy(bill, t_bill)

    resbuff = db_session.query(Resbuff).filter(
            (Resbuff.resnr == bill.resnr) &  (Resbuff.reslinnr == bill.parent_nr)).first()

    if resbuff:
        abreise = resbuff.abreise
    else:
        abreise = bill.datum

    if res_line and bil_flag == 0 and res_line.abreise == ci_date:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "flag") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.betriebsnr == 0) &  ((Reslin_queasy.logi1) |  (Reslin_queasy.logi2) |  (Reslin_queasy.logi3 ))).first()

        if reslin_queasy:
            flag_report = True

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == bill.resnr)).first()
    resname = ""

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == bill.gastnr)).first()
    g_address = guest.adresse1
    g_wonhort = guest.wohnort
    g_plz = guest.plz
    g_land = guest.land

    if g_address == None:
        g_address = ""

    if g_wonhort == None:
        g_wonhort = ""

    if g_plz == None:
        g_plz = ""

    if g_land == None:
        g_land = ""
    resname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1 + chr (10) + g_address + chr (10) + g_wonhort + " " + g_plz + chr (10) + g_land

    if guest.kreditlimit != 0:
        kreditlimit = guest.kreditlimit
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 68)).first()

        if htparam.fdecimal != 0:
            kreditlimit = htparam.fdecimal
        else:
            kreditlimit = htparam.finteger

    zimmer = db_session.query(Zimmer).filter(
            (Zimmer.zinr == bill.zinr)).first()
    zimmer_bezeich = zimmer.bezeich
    res_exrate = 1

    if res_line:

        if res_line.reserve_dec != 0:
            res_exrate = res_line.reserve_dec
        else:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == res_line.betriebsnr)).first()

            if waehrung:
                res_exrate = waehrung.ankauf / waehrung.einheit

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 700)).first()

    if htparam.finteger != 0:
        vipnr1 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 701)).first()

    if htparam.finteger != 0:
        vipnr2 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 702)).first()

    if htparam.finteger != 0:
        vipnr3 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 703)).first()

    if htparam.finteger != 0:
        vipnr4 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 704)).first()

    if htparam.finteger != 0:
        vipnr5 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 705)).first()

    if htparam.finteger != 0:
        vipnr6 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 706)).first()

    if htparam.finteger != 0:
        vipnr7 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 707)).first()

    if htparam.finteger != 0:
        vipnr8 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 708)).first()

    if htparam.finteger != 0:
        vipnr9 = finteger
    check_vip(bill.gastnr)

    if not vipflag and guestmember:
        check_vip(guestmember.gastnr)
    master_str = ""
    master_rechnr = ""

    master = db_session.query(Master).filter(
            (Master.resnr == bill.resnr)).first()

    if master:

        mbill = db_session.query(Mbill).filter(
                (Mbill.resnr == bill.resnr) &  (Mbill.reslinnr == 0) &  (Mbill.zinr == "")).first()

        if not mbill:

            counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 3)).first()
            counters = counters + 1

            counters = db_session.query(Counters).first()
            mbill = Mbill()
            db_session.add(mbill)

            mbill.rechnr = counters

            mbill = db_session.query(Mbill).first()

            master = db_session.query(Master).first()
            master.rechnr = mbill.rechnr

            master = db_session.query(Master).first()

        if mbill:
            master_str = "Master Bill"
            master_rechnr = to_string(mbill.rechnr) + " - " + mbill.name
    bill_anzahl = 0

    if bill.flag == 0:

        for bill1 in db_session.query(Bill1).filter(
                    (Bill1.resnr == bill.resnr) &  (Bill1.parent_nr == bill.parent_nr) &  (Bill1.parent_nr != 0) &  (Bill1.flag == 0) &  (Bill1.zinr == bill.zinr)).all():
            bill_anzahl = bill_anzahl + 1


    if res_line and res_line.code != "" and bill.flag == 0:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

        if queasy and queasy.logi1:
            queasy_char1 = queasy.char1

    return generate_output()