from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.create_historybl import create_historybl
from functions.intevent_1 import intevent_1
from models import Res_line, Bill, Guest, Reservation, Bediener, Htparam, Outorder, Bill_line, Reslin_queasy, Zimmer, Guestat, Akt_cust, Salestat, Res_history, Zimplan, Resplan, Mealcoup, Queasy, Master

def inv_checkout_listbl(pvilanguage:int, case_type:int, resnr:int, reslinnr:int, user_init:str, reason_str:str, silenzio:bool):
    error_code = 0
    checked_out = False
    early_co = False
    goto_master = False
    flag_report = False
    msg_str = ""
    msg_int = 0
    min_reslinnr:int = 0
    pax:int = 0
    rechnr:int = 0
    rm_nite:int = 0
    co_date:date = None
    bill_date:date = None
    zinr:str = ""
    add_str:str = ""
    main_guest:bool = False
    co_ok:bool = False
    zugriff:bool = False
    answer:bool = True
    room_added:bool = False
    do_it:bool = False
    statusstr:str = ""
    unbalanced_bill:bool = False
    priscilla_active:bool = True
    lvcarea:str = "inv_checkout_listbl"
    bl_saldo:decimal = 0
    res_line = bill = guest = reservation = bediener = htparam = outorder = bill_line = reslin_queasy = zimmer = guestat = akt_cust = salestat = res_history = zimplan = resplan = mealcoup = queasy = master = None

    resline = mbill = rguest = rline = tbuff = bill1 = res_line1 = res_line2 = sharer = None

    Resline = Res_line
    Mbill = Bill
    Rguest = Guest
    Rline = Res_line
    Tbuff = Bill
    Bill1 = Bill
    Res_line1 = Res_line
    Res_line2 = Res_line
    Sharer = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, checked_out, early_co, goto_master, flag_report, msg_str, msg_int, min_reslinnr, pax, rechnr, rm_nite, co_date, bill_date, zinr, add_str, main_guest, co_ok, zugriff, answer, room_added, do_it, statusstr, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, res_line, bill, guest, reservation, bediener, htparam, outorder, bill_line, reslin_queasy, zimmer, guestat, akt_cust, salestat, res_history, zimplan, resplan, mealcoup, queasy, master
        nonlocal resline, mbill, rguest, rline, tbuff, bill1, res_line1, res_line2, sharer


        nonlocal resline, mbill, rguest, rline, tbuff, bill1, res_line1, res_line2, sharer
        return {"error_code": error_code, "checked_out": checked_out, "early_co": early_co, "goto_master": goto_master, "flag_report": flag_report, "msg_str": msg_str, "msg_int": msg_int}

    def check_billstatus():

        nonlocal error_code, checked_out, early_co, goto_master, flag_report, msg_str, msg_int, min_reslinnr, pax, rechnr, rm_nite, co_date, bill_date, zinr, add_str, main_guest, co_ok, zugriff, answer, room_added, do_it, statusstr, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, res_line, bill, guest, reservation, bediener, htparam, outorder, bill_line, reslin_queasy, zimmer, guestat, akt_cust, salestat, res_history, zimplan, resplan, mealcoup, queasy, master
        nonlocal resline, mbill, rguest, rline, tbuff, bill1, res_line1, res_line2, sharer


        nonlocal resline, mbill, rguest, rline, tbuff, bill1, res_line1, res_line2, sharer

        co_ok = False
        parent_nr:int = 0

        def generate_inner_output():
            return co_ok
        Bill1 = Bill

        if unbalanced_bill == False:

            bill1 = db_session.query(Bill1).filter(
                    (Bill1.resnr == resnr) &  (Bill1.reslinnr == reslinnr) &  (Bill1.flag == 0) &  (func.lower(Bill1.(zinr).lower()) == (zinr).lower())).first()

            if bill1:
                parent_nr = bill1.parent_nr

                for bill1 in db_session.query(Bill1).filter(
                        (Bill1.resnr == resnr) &  (Bill1.parent_nr == parent_nr) &  (Bill1.flag == 0)).all():

                    bill_line = db_session.query(Bill_line).filter(
                            (Bill_line.rechnr == bill1.rechnr)).first()

                    if bill_line and co_ok and (bill1.rgdruck == 0 or bill1.saldo != 0):
                        co_ok = False
                        rechnr = bill1.rechnr

                        if bill1.saldo != 0:
                            error_code = 1
                            msg_str = translateExtended ("RoomNo", lvcarea, "") +\
                                " " + zinr + "  -  " +\
                                translateExtended ("BillNo", lvcarea, "") +\
                                " " + to_string(rechnr) + " " +\
                                translateExtended ("not yet balanced", lvcarea, "") + chr(10) +\
                                translateExtended ("Check_out not possible.", lvcarea, "") + chr(10)


                        else:
                            error_code = 2
                            msg_str = translateExtended ("RoomNo", lvcarea, "") +\
                                " " + zinr + "  -  " +\
                                translateExtended ("BillNo", lvcarea, "") +\
                                " " + to_string(rechnr) + " " +\
                                translateExtended ("not yet printed.", lvcarea, "") + chr(10) +\
                                translateExtended ("Check_out not possible.", lvcarea, "") + chr(10)

                        return generate_inner_output()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 141)).first()

        if htparam.fchar != "":

            resline = db_session.query(Resline).filter(
                    (Resline.resnr == resnr) &  (Resline.active_flag == 1) &  (Resline.resstatus != 12) &  (Resline.reslinnr != reslinnr)).first()

            if not resline:

                mbill = db_session.query(Mbill).filter(
                        (Mbill.resnr == resnr) &  (Mbill.zinr == "") &  (Mbill.flag == 0)).first()

                if mbill and mbill.saldo > 0:

                    rguest = db_session.query(Rguest).filter(
                            (Rguest.gastnr == mbill.gastnr)).first()

                    if rguest.zahlungsart == 0:
                        error_code = 3
                        co_ok = False
                        msg_str = translateExtended ("RoomNo", lvcarea, "") +\
                            " " + zinr + "  -  " +\
                            translateExtended ("Master Bill not yet settled.", lvcarea, "") + chr(10) +\
                            translateExtended ("Check_out not possible.", lvcarea, "") + chr(10)


        return generate_inner_output()

    def check_co_time():

        nonlocal error_code, checked_out, early_co, goto_master, flag_report, msg_str, msg_int, min_reslinnr, pax, rechnr, rm_nite, co_date, bill_date, zinr, add_str, main_guest, co_ok, zugriff, answer, room_added, do_it, statusstr, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, res_line, bill, guest, reservation, bediener, htparam, outorder, bill_line, reslin_queasy, zimmer, guestat, akt_cust, salestat, res_history, zimplan, resplan, mealcoup, queasy, master
        nonlocal resline, mbill, rguest, rline, tbuff, bill1, res_line1, res_line2, sharer


        nonlocal resline, mbill, rguest, rline, tbuff, bill1, res_line1, res_line2, sharer

        co_zeit:int = 0
        co_datum:date = None
        zeit:int = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1076)).first()

        if htparam.feldtyp == 4 and htparam.flogical:
            co_zeit = res_line.abreisezeit

            if co_zeit == 0:
                co_zeit = 12 * 3600
            co_datum = res_line.abreise
            zeit = get_current_time_in_seconds()

            if (co_datum == bill_date) and (zeit > co_zeit):
                msg_int = 4
                msg_str = translateExtended ("C/O Time", lvcarea, "") + " " + to_string(co_zeit, "HH:MM:SS") + " " + translateExtended ("exceeded. Current time is", lvcarea, "") + " " + to_string(zeit, "HH:MM:SS") + chr(10) + translateExtended ("Exceeded time  == ", lvcarea, "") + " " + to_string((zeit - co_zeit) , "HH:MM:SS") + chr(10)

    def guest_checkout():

        nonlocal error_code, checked_out, early_co, goto_master, flag_report, msg_str, msg_int, min_reslinnr, pax, rechnr, rm_nite, co_date, bill_date, zinr, add_str, main_guest, co_ok, zugriff, answer, room_added, do_it, statusstr, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, res_line, bill, guest, reservation, bediener, htparam, outorder, bill_line, reslin_queasy, zimmer, guestat, akt_cust, salestat, res_history, zimplan, resplan, mealcoup, queasy, master
        nonlocal resline, mbill, rguest, rline, tbuff, bill1, res_line1, res_line2, sharer


        nonlocal resline, mbill, rguest, rline, tbuff, bill1, res_line1, res_line2, sharer

        ankunft:date = None
        abreise:date = None
        resstatus:int = 0
        res_recid:int = 0
        res_recid1:int = 0
        tot_umsatz:decimal = 0
        day_use:bool = False
        real_guest:bool = True
        sales_lic:bool = False
        dummy_logi:bool = False
        sharer_co:bool = False
        Bill1 = Bill
        Rline = Res_line
        Res_line1 = Res_line
        Res_line2 = Res_line
        Sharer = Res_line

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "flag") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.reslinnr == reslinnr) &  (Reslin_queasy.betriebsnr == 0)).first()

        if reslin_queasy and (reslin_queasy.logi1  or reslin_queasy.logi2  or reslin_queasy.logi3 ):
            flag_report = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1002)).first()
        sales_lic = htparam.flogical

        if res_line.betrieb_gast > 0:
            msg_int = 5
            msg_str = translateExtended ("Number of created KeyCard(s)  == ", lvcarea, "") + " " + to_string(res_line.betrieb_gast) + chr(10)

        zimmer = db_session.query(Zimmer).filter(
                (func.lower(Zimmer.(zinr).lower()) == (zinr).lower())).first()

        res_line1 = db_session.query(Res_line1).filter(
                (Res_line1._recid != res_line._recid) &  (func.lower(Res_line1.(zinr).lower()) == (zinr).lower()) &  ((Res_line1.resstatus == 6) |  (Res_line1.resstatus == 13)) &  (Res_line1.l_zuordnung[2] == 0)).first()

        if not res_line1:

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == zimmer.zinr) &  (Outorder.gespstart <= co_date) &  (Outorder.gespende >= co_date) &  (Outorder.betriebsnr <= 1)).first()

            zimmer = db_session.query(Zimmer).first()

            if outorder:
                zimmer.zistatus = 6
                zimmer.bediener_nr_stat = 0


            else:
                zimmer.zistatus = 2
                zimmer.bediener_nr_stat = 0

            zimmer = db_session.query(Zimmer).first()


        for bill1 in db_session.query(Bill1).filter(
                (Bill1.resnr == resnr) &  (Bill1.parent_nr == reslinnr) &  (Bill1.flag == 0) &  (func.lower(Bill1.(zinr).lower()) == (zinr).lower())).all():
            tot_umsatz = tot_umsatz + bill1.gesamtumsatz

        if (co_date - res_line.ankunft) == 0 and tot_umsatz == 0:
            real_guest = False

        for sharer in db_session.query(Sharer).filter(
                    (Sharer.resnr == resnr) &  (Sharer.kontakt_nr == reslinnr) &  (Sharer.l_zuordnung[2] == 1) &  (Sharer.active_flag <= 1)).all():

            if real_guest:
                get_output(create_historybl(sharer.resnr, sharer.reslinnr, sharer.zinr, "checkout", user_init, ""))
            sharer.active_flag = 2
            sharer.resstatus = 8
            sharer.abreise = co_date
            sharer.abreisezeit = get_current_time_in_seconds()
            sharer.changed = co_date
            sharer.changed_id = user_init

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 307)).first()

        if htparam.flogical:
            get_output(intevent_1(2, zinr, "My Checkout!", res_line.resnr, res_line.reslinnr))

        if priscilla_active:
            get_output(intevent_1(2, zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        for bill1 in db_session.query(Bill1).filter(
                    (Bill1.resnr == resnr) &  (Bill1.parent_nr == reslinnr) &  (Bill1.flag == 0)).all():
            bl_saldo = 0

            for bill_line in db_session.query(Bill_line).filter(
                        (Bill_line.rechnr == bill1.rechnr)).all():
                bl_saldo = bl_saldo + bill_line.betrag

            if bl_saldo != bill1.saldo:

                tbuff = db_session.query(Tbuff).filter(
                            (Tbuff._recid == bill1._recid)).first()
                tbuff.saldo = bl_saldo

                tbuff = db_session.query(Tbuff).first()

            bill1.vesrcod = user_init
            bill1.flag = 1
            bill1.datum = co_date

        for bill1 in db_session.query(Bill1).filter(
                    (Bill1.resnr == resnr) &  (Bill1.parent_nr == reslinnr) &  (func.lower(Bill1.(zinr).lower()) == (zinr).lower())).all():

            if real_guest and resstatus != 12:
                get_output(create_historybl(resnr, reslinnr, zinr, "checkout", user_init, ""))

            res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == bill1.resnr) &  (Res_line.reslinnr == bill1.reslinnr) &  (Res_line.zinr == bill1.zinr)).first()
            res_recid = res_line._recid
            resstatus = res_line.resstatus
            ankunft = res_line.ankunft
            abreise = res_line.abreise

            if res_line.resstatus != 12:
                res_line.resstatus = 8
            res_line.abreise = co_date
            res_line.abreisezeit = get_current_time_in_seconds()
            res_line.changed = co_date
            res_line.changed_id = user_init
            res_line.active_flag = 2

            if reason_str != "" and reason_str != None:
                res_line.zimmer_wunsch = res_line.zimmer_wunsch + "earlyCO," + reason_str + ";"

            res_line2 = db_session.query(Res_line2).filter(
                        (Res_line2.resnr == res_line.resnr) &  (Res_line2.active_flag < 2)).first()

            if not res_line2:

                reservation = db_session.query(Reservation).first()
                reservation.activeflag = 1

                reservation = db_session.query(Reservation).first()

            if tot_umsatz != 0:

                guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnrpay)).first()
                guest.logisumsatz = guest.logisumsatz + bill1.logisumsatz
                guest.argtumsatz = guest.argtumsatz + bill1.argtumsatz
                guest.f_b_umsatz = guest.f_b_umsatz + bill1.f_b_umsatz
                guest.sonst_umsatz = guest.sonst_umsatz + bill1.sonst_umsatz
                guest.gesamtumsatz = guest.gesamtumsatz + bill1.gesamtumsatz


                guestat = db_session.query(Guestat).filter(
                                (Guestat.gastnr == res_line.gastnr) &  (Guestat.monat == get_month(bill_date)) &  (Guestat.jahr == get_year(bill_date)) &  (Guestat.betriebsnr == 0)).first()

                if not guestat:
                    guestat = Guestat()
                    db_session.add(guestat)

                    guestat.gastnr = res_line.gastnr
                    guestat.monat = get_month(bill_date)
                    guestat.jahr = get_year(bill_date)


                guestat.logisumsatz = guestat.logisumsatz + bill1.logisumsatz
                guestat.argtumsatz = guestat.argtumsatz + bill1.argtumsatz
                guestat.f_b_umsatz = guestat.f_b_umsatz + bill1.f_b_umsatz
                guestat.sonst_umsatz = guestat.sonst_umsatz + bill1.sonst_umsatz
                guestat.gesamtumsatz = guestat.gesamtumsatz + bill1.gesamtumsatz

                guestat = db_session.query(Guestat).first()

                akt_cust = db_session.query(Akt_cust).filter(
                                (Akt_cust.gastnr == res_line.gastnr)).first()

                if akt_cust:

                    bediener = db_session.query(Bediener).filter(
                                    (Bediener.userinit == akt_cust.userinit)).first()

                if not akt_cust or not bediener:

                    rguest = db_session.query(Rguest).filter(
                                    (Rguest.gastnr == res_line.gastnr)).first()

                    if rguest.phonetik3 != "":

                        bediener = db_session.query(Bediener).filter(
                                        (Bediener.userinit == rguest.phonetik3)).first()

                if bediener:

                    salestat = db_session.query(Salestat).filter(
                                    (Salestat.bediener_nr == bediener.nr) &  (Salestat.jahr == get_year(bill_date)) &  (Salestat.monat == get_month(bill_date))).first()

                    if not salestat:
                        salestat = Salestat()
                        db_session.add(salestat)

                        salestat.bediener_nr = bediener.nr
                        salestat.jahr = get_year(bill_date)
                        salestat.monat = get_month(bill_date)


                    salestat.logisumsatz = salestat.logisumsatz + bill1.logisumsatz
                    salestat.argtumsatz = salestat.argtumsatz + bill1.argtumsatz
                    salestat.f_b_umsatz = salestat.f_b_umsatz + bill1.f_b_umsatz
                    salestat.sonst_umsatz = salestat.sonst_umsatz + bill1.sonst_umsatz
                    salestat.gesamtumsatz = salestat.gesamtumsatz + bill1.gesamtumsatz

                    if res_line.resstatus != 12:
                        salestat.room_nights = salestat.room_nights + (co_date - ankunft)

                        if (co_date - ankunft) == 0:
                            salestat.room_nights = salestat.room_nights + 1

                    salestat = db_session.query(Salestat).first()

            if real_guest and res_line.resstatus != 12:

                guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnrmember)).first()
                guest.date1 = res_line.ankunft
                guest.date2 = res_line.abreise
                guest.zimmeranz = guest.zimmeranz + 1
                guest.resflag = 0

                rline = db_session.query(Rline).filter(
                            (Rline.resstatus == 8) &  (Rline.abreise == co_date) &  (Rline.gastnrmember == guest.gastnr) &  (((Rline.resnr != res_line.resnr)) |  ((Rline.reslinnr != res_line.reslinnr)))).first()

                if not rline:
                    guest.aufenthalte = guest.aufenthalte + 1

                guest = db_session.query(Guest).first()

                if res_line.gastnrmember != res_line.gastnr:
                    get_min_reslinnr()

                    guest = db_session.query(Guest).filter(
                                (Guest.gastnr == res_line.gastnr)).first()
                    guest.zimmeranz = guest.zimmeranz + 1

                    if min_reslinnr == 1:
                        guest.aufenthalte = guest.aufenthalte + 1

                    guest = db_session.query(Guest).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.resnr = res_line.resnr
                res_history.reslinnr = res_line.reslinnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "CheckOut Room " + res_line.zinr +\
                        " ResNo " + to_string(res_line.resnr)
                res_history.action = "CheckOut"

                res_line = db_session.query(Res_line).first()

            else:
                res_line.cancelled = co_date

            res_recid1 = 0

            for zimplan in db_session.query(Zimplan).filter(
                        (Zimplan.datum >= co_date) &  (Zimplan.datum < abreise) &  (func.lower(Zimplan.(zinr).lower()) == (zinr).lower()) &  (Zimplan.res_recid == res_recid)).all():

                if res_recid1 != 0:

                    if zimplan.datum < res_line1.abreise:
                        zimplan.res_recid = res_recid1
                    else:
                        db_session.delete(zimplan)

            if resstatus != 12:

                for resplan in db_session.query(Resplan).filter(
                            (Resplan.datum >= co_date) &  (Resplan.datum < abreise) &  (Resplan.zikatnr == zimmer.zikatnr)).all():
                    resplan.anzzim[resstatus - 1] = resplan.anzzim[resstatus - 1] - 1


            resline = db_session.query(Resline).filter(
                        (Resline.resnr == resnr) &  ((Resline.active_flag == 0) |  (Resline.active_flag == 1)) &  (Resline.resstatus != 12)).first()

            if not resline:

                mealcoup = db_session.query(Mealcoup).filter(
                            (func.lower(Mealcoup.(zinr).lower()) == (zinr).lower()) &  (Mealcoup.activeflag)).first()

                if mealcoup:
                    mealcoup.activeflag = False
                    mealcoup.abreise = get_current_date()

                    mealcoup = db_session.query(Mealcoup).first()

            for queasy in db_session.query(Queasy).filter(
                        (Queasy.key == 16) &  (Queasy.number1 == resnr) &  (Queasy.number2 == reslinnr)).all():
                db_session.delete(queasy)

        res_line1 = db_session.query(Res_line1).filter(
                    ((Res_line1.resnr == resnr)) &  ((Res_line1.reslinnr != reslinnr)) &  ((Res_line1.resstatus == 6) |  (Res_line1.resstatus == 13))).first()

        if not res_line1:

            master = db_session.query(Master).filter(
                        (Master.resnr == resnr)).first()

            if master:
                master.active = False

                master = db_session.query(Master).first()

                bill1 = db_session.query(Bill1).filter(
                            (Bill1.resnr == resnr) &  (Bill1.reslinnr == 0)).first()

                if bill1 and bill1.rechnr != 0:

                    guest = db_session.query(Guest).filter(
                                (Guest.gastnr == bill1.gastnr)).first()
                    guest.logisumsatz = guest.logisumsatz + bill1.logisumsatz
                    guest.argtumsatz = guest.argtumsatz + bill1.argtumsatz
                    guest.f_b_umsatz = guest.f_b_umsatz + bill1.f_b_umsatz
                    guest.sonst_umsatz = guest.sonst_umsatz + bill1.sonst_umsatz
                    guest.gesamtumsatz = guest.gesamtumsatz + bill1.gesamtumsatz


            for queasy in db_session.query(Queasy).filter(
                        (Queasy.key == 24) &  (func.lower(Queasy.char1) == (zinr).lower())).all():
                db_session.delete(queasy)

        checked_out = True
        msg_int = 6
        msg_str = translateExtended ("Guest checked_out.", lvcarea, "") + chr(10)

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

        if not silenzio:

            resline = db_session.query(Resline).filter(
                    (Resline.resnr == resnr) &  (Resline.active_flag == 1) &  (Resline.zinr == res_line.zinr) &  (Resline.l_zuordnung[2] == 0) &  (Resline.abreise == co_date)).first()

            if resline:

                if resline.resstatus == 6:
                    statusstr = translateExtended ("Status: Main Guest; RmRate  == ", lvcarea, "")
                else:
                    statusstr = translateExtended ("Status: Room Sharer; RmRate  == ", lvcarea, "")
                    msg_int = 7
                    msg_str = translateExtended ("Other Expected Departure Guest FOUND in the same room:", lvcarea, "") + chr(10) + resline.name + " " + to_string(resline.ankunft) + " - " + to_string(resline.abreise) + chr(10) + statusstr + " " + to_string(resline.zipreis)

        mbill = db_session.query(Mbill).filter(
                (Mbill.resnr == resnr) &  (Mbill.zinr == "")).first()

        if not mbill and res_line.l_zuordnung[4] != 0 and res_line.l_zuordnung[1] == 0:

            mbill = db_session.query(Mbill).filter(
                    (Mbill.resnr == res_line.l_zuordnung[4]) &  (Mbill.zinr == "") &  (Mbill.flag == 0)).first()

        if mbill:

            resline = db_session.query(Resline).filter(
                    (Resline.resnr == mbill.resnr) &  (Resline.active_flag <= 1)).first()

            if not resline:

                if res_line.l_zuordnung[4] == 0:
                    goto_master = True
                else:

                    resline = db_session.query(Resline).filter(
                            (Resline.resnr != mbill.resnr) &  (Resline.active_flag == 1) &  (Resline.l_zuordnung[1] == 0) &  (Resline.l_zuordnung[4] == mbill.resnr)).first()
                    goto_master = not None != resline

        if goto_master:
            msg_int = 8
            msg_str = translateExtended ("All guests are checked_out, close the master bill NOW?", lvcarea, "") + chr(10) + translateExtended ("BillNo :", lvcarea, "") + " " + to_string(mbill.rechnr) + " " + translateExtended ("- ResNo :", lvcarea, "") + " " + to_string(mbill.resnr) + chr(10)

    def get_min_reslinnr():

        nonlocal error_code, checked_out, early_co, goto_master, flag_report, msg_str, msg_int, min_reslinnr, pax, rechnr, rm_nite, co_date, bill_date, zinr, add_str, main_guest, co_ok, zugriff, answer, room_added, do_it, statusstr, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, res_line, bill, guest, reservation, bediener, htparam, outorder, bill_line, reslin_queasy, zimmer, guestat, akt_cust, salestat, res_history, zimplan, resplan, mealcoup, queasy, master
        nonlocal resline, mbill, rguest, rline, tbuff, bill1, res_line1, res_line2, sharer


        nonlocal resline, mbill, rguest, rline, tbuff, bill1, res_line1, res_line2, sharer


        Resline = Res_line

        for resline in db_session.query(Resline).filter(
                (Resline.resnr == resnr) &  (Resline.active_flag == 1) &  (Resline.resstatus != 12)).all():
            min_reslinnr = min_reslinnr + 1


    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    co_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 974)).first()
    unbalanced_bill = htparam.flogical

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()
    zinr = res_line.zinr
    pax = res_line.erwachs
    main_guest = (res_line.resstatus == 6)


    co_ok = check_billstatus()

    if not co_ok:

        return generate_output()

    if case_type == 1:

        rline = db_session.query(Rline).filter(
                (Rline.active_flag == 1) &  (Rline.zinr == res_line.zinr) &  (Rline.l_zuordnung[2] == 0) &  (Rline._recid == res_line._recid)).first()

        if rline:

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == res_line.zinr) &  (Outorder.gespstart <= co_date) &  (Outorder.gespende >= co_date) &  (Outorder.betriebsnr <= 1)).first()

            if outorder:
                msg_int = 1
                msg_str = translateExtended ("Out_Of_Order Record found for this room:", lvcarea, "") + " " + to_string(outorder.gespstart) + "-" + to_string(outorder.gespende) + chr(10) + translateExtended ("The room status will immediately be changed to O_O_O after checking_out the guest.", lvcarea, "") + chr(10)
            early_co = (res_line.abreise > co_date)
            check_co_time()

            if early_co:

                if substring(bediener.perm, 69, 1) >= "2":
                    msg_int = 2
                    msg_str = translateExtended ("Early Check_out", lvcarea, "") + " " + res_line.name + chr(10) + translateExtended ("ROOM", lvcarea, "") + " " + res_line.zinr + " ?" + chr(10)
                else:
                    msg_str = translateExtended ("No Access Right for Early Checkout [70,2].", lvcarea, "") + chr(10)
                    error_code = 4
            else:
                msg_int = 3
                msg_str = translateExtended ("Check_out", lvcarea, "") + " " + res_line.name + chr(10) + translateExtended ("ROOM", lvcarea, "") + " " + res_line.zinr + " ?" + chr(10)

        return generate_output()
    guest_checkout()

    return generate_output()