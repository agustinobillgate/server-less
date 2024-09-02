from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.intevent_1 import intevent_1
from functions.create_historybl import create_historybl
from models import Bediener, Htparam, Bill, Reservation, Res_line, Reslin_queasy, Guest, Arrangement, Bill_line, Zimmer, Res_history, Outorder, Guestat, Akt_cust, Salestat, Zimplan, Resplan, Mealcoup, Queasy, Master

def res_checkoutbl(pvilanguage:int, case_type:int, resnr:int, reslinnr:int, silenzio:bool, user_init:str):
    co_ok = False
    checked_out = False
    flag_report = False
    msg_str = ""
    co_date:date = None
    min_reslinnr:int = 0
    real_guest:bool = True
    main_guest:bool = False
    unbalanced_bill:bool = False
    priscilla_active:bool = True
    lvcarea:str = "res_checkout"
    bl_saldo:decimal = 0
    bediener = htparam = bill = reservation = res_line = reslin_queasy = guest = arrangement = bill_line = zimmer = res_history = outorder = guestat = akt_cust = salestat = zimplan = resplan = mealcoup = queasy = master = None

    usr1 = tbuff = bill1 = res_line1 = res_line2 = rline = resline = sharer = rguest = mbill = None

    Usr1 = Bediener
    Tbuff = Bill
    Bill1 = Bill
    Res_line1 = Res_line
    Res_line2 = Res_line
    Rline = Res_line
    Resline = Res_line
    Sharer = Res_line
    Rguest = Guest
    Mbill = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal co_ok, checked_out, flag_report, msg_str, co_date, min_reslinnr, real_guest, main_guest, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, bediener, htparam, bill, reservation, res_line, reslin_queasy, guest, arrangement, bill_line, zimmer, res_history, outorder, guestat, akt_cust, salestat, zimplan, resplan, mealcoup, queasy, master
        nonlocal usr1, tbuff, bill1, res_line1, res_line2, rline, resline, sharer, rguest, mbill


        nonlocal usr1, tbuff, bill1, res_line1, res_line2, rline, resline, sharer, rguest, mbill
        return {"co_ok": co_ok, "checked_out": checked_out, "flag_report": flag_report, "msg_str": msg_str}

    def check_billstatus():

        nonlocal co_ok, checked_out, flag_report, msg_str, co_date, min_reslinnr, real_guest, main_guest, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, bediener, htparam, bill, reservation, res_line, reslin_queasy, guest, arrangement, bill_line, zimmer, res_history, outorder, guestat, akt_cust, salestat, zimplan, resplan, mealcoup, queasy, master
        nonlocal usr1, tbuff, bill1, res_line1, res_line2, rline, resline, sharer, rguest, mbill


        nonlocal usr1, tbuff, bill1, res_line1, res_line2, rline, resline, sharer, rguest, mbill

        parent_nr:int = 0
        co_str:str = ""
        Bill1 = Bill

        if unbalanced_bill == False:

            bill1 = db_session.query(Bill1).filter(
                    (Bill1.resnr == resnr) &  (Bill1.parent_nr == reslinnr) &  (Bill1.flag == 0) &  ((Bill1.saldo != 0) |  (Bill1.rgdruck == 0))).first()

            if bill1:
                co_ok = False

                if bill1.saldo != 0:
                    msg_str = translateExtended ("RoomNo", lvcarea, "") +\
                        " " + res_line.zinr + "  -  " +\
                        translateExtended ("BillNo", lvcarea, "") +\
                        " " + to_string(bill1.rechnr) +\
                        " " + translateExtended ("not yet balanced", lvcarea, "") + chr(10) +\
                        translateExtended ("Check_out not possible.", lvcarea, "")


                else:
                    msg_str = translateExtended ("RoomNo", lvcarea, "") +\
                        " " + res_line.zinr + "  -  " +\
                        translateExtended ("BillNo", lvcarea, "") +\
                        " " + to_string(bill1.rechnr) +\
                        " " + translateExtended ("not yet printed", lvcarea, "") + chr(10) +\
                        translateExtended ("Check_out not possible.", lvcarea, "")

            if not co_ok:

                return

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if res_line.abreise > co_date:
            co_ok = substring(bediener.permissions, 69, 1) >= "2"
            co_str = translateExtended ("EARLY Check_out", lvcarea, "")


        else:
            co_ok = True
            co_str = translateExtended ("Check_out", lvcarea, "")

        if not silenzio and co_ok:
            msg_str = "&Q" + co_str + " " + res_line.name + chr(10) + translateExtended ("ROOM", lvcarea, "") + " " + res_line.zinr + " ?"

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "flag") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.reslinnr == reslinnr) &  (Reslin_queasy.betriebsnr == 0)).first()

            if reslin_queasy and (reslin_queasy.logi1  or reslin_queasy.logi2  or reslin_queasy.logi3 ):
                flag_report = True

    def guest_checkout():

        nonlocal co_ok, checked_out, flag_report, msg_str, co_date, min_reslinnr, real_guest, main_guest, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, bediener, htparam, bill, reservation, res_line, reslin_queasy, guest, arrangement, bill_line, zimmer, res_history, outorder, guestat, akt_cust, salestat, zimplan, resplan, mealcoup, queasy, master
        nonlocal usr1, tbuff, bill1, res_line1, res_line2, rline, resline, sharer, rguest, mbill


        nonlocal usr1, tbuff, bill1, res_line1, res_line2, rline, resline, sharer, rguest, mbill

        ankunft:date = None
        abreise:date = None
        resstatus:int = 0
        res_recid:int = 0
        res_recid1:int = 0
        tot_umsatz:decimal = 0
        day_use:bool = False
        dummy_logi:bool = False
        pax:int = 0
        zinr:str = ""
        bill_date:date = None
        Bill1 = Bill
        Res_line1 = Res_line
        Res_line2 = Res_line
        Rline = Res_line
        Resline = Res_line
        Sharer = Res_line
        Rguest = Guest
        Mbill = Bill

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate
        zinr = res_line.zinr
        pax = res_line.erwachs
        main_guest = (res_line.resstatus == 6)

        if main_guest and (res_line.abreise > co_date) and not silenzio:

            sharer = db_session.query(Sharer).filter(
                    (Sharer.resnr == res_line.resnr) &  (Sharer.zinr == res_line.zinr) &  (Sharer.resstatus == 13) &  (Sharer.abreise > co_date) &  (Sharer.zipreis == 0)).first()

            if sharer:
                msg_str = "&W" + translateExtended ("Room sharer found with ZERO rate for room", lvcarea, "") + " " + res_line.zinr + chr(10) + translateExtended ("Change room sharer status and update the Rate.", lvcarea, "") + chr(10)

        if co_date == res_line.ankunft:

            if res_line.l_zuordnung[2] == 1:
                real_guest = False
            else:

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()

                bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.departement == 0) &  (Bill_line.artnr == arrangement.argt_artikelnr) &  (Bill_line.bill_datum == bill_date) &  (Bill_line.massnr == res_line.resnr) &  (Bill_line.billin_nr == res_line.reslinnr)).first()
                real_guest = None != bill_line

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 307)).first()

        if htparam.flogical:
            get_output(intevent_1(2, res_line.zinr, "My Checkout!", res_line.resnr, res_line.reslinnr))

        if priscilla_active:
            get_output(intevent_1(2, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        zimmer = db_session.query(Zimmer).filter(
                (func.lower(Zimmer.(zinr).lower()) == (zinr).lower())).first()

        usr1 = db_session.query(Usr1).filter(
                (func.lower(Usr1.userinit) == (user_init).lower())).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = usr1.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "C/O " +\
                "Room " + zimmer.zinr +\
                " Status Changed From " +\
                to_string(zimmer.zistatus) + " to Vacant Dirty"
        res_history.action = "FO Cashier"

        res_history = db_session.query(Res_history).first()


        res_line1 = db_session.query(Res_line1).filter(
                (Res_line1._recid != res_line._recid) &  (func.lower(Res_line1.(zinr).lower()) == (zinr).lower()) &  ((Res_line1.resstatus == 6) |  (Res_line1.resstatus == 13)) &  (Res_line1.l_zuordnung[2] == 0)).first()

        if not res_line1:

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == zimmer.zinr) &  (Outorder.gespstart <= co_date) &  (Outorder.gespende >= co_date) &  (Outorder.betriebsnr <= 1)).first()

            zimmer = db_session.query(Zimmer).first()

            if not outorder:
                zimmer.zistatus = 2
                zimmer.bediener_nr_stat = 0


            else:
                zimmer.zistatus = 6
                zimmer.bediener_nr_stat = 0

            zimmer = db_session.query(Zimmer).first()

        for bill1 in db_session.query(Bill1).filter(
                (Bill1.resnr == resnr) &  (Bill1.parent_nr == reslinnr) &  (Bill1.flag == 0) &  (Bill1.zinr == res_line.zinr)).all():
            tot_umsatz = tot_umsatz + bill1.gesamtumsatz

        bill1 = db_session.query(Bill1).filter(
                (Bill1.resnr == resnr) &  (Bill1.parent_nr == reslinnr) &  (Bill1.zinr == res_line.zinr)).first()

        if not bill1:

            res_line1 = db_session.query(Res_line1).filter(
                    (Res_line1._recid == res_line._recid)).first()
            res_line1.resstatus = 8
            res_line1.abreise = co_date
            res_line1.abreisezeit = get_current_time_in_seconds()
            res_line1.changed = co_date
            res_line1.changed_id = user_init
            res_line1.active_flag = 2

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line1.gastnrmember)).first()
            guest.date1 = res_line1.ankunft
            guest.date2 = res_line1.abreise
            guest.zimmeranz = guest.zimmeranz + 1
            guest.resflag = 0

            rline = db_session.query(Rline).filter(
                    (Rline.resstatus == 8) &  (Rline.abreise == co_date) &  (Rline.gastnrmember == guest.gastnr) &  (((Rline.resnr != res_line.resnr)) |  ((Rline.reslinnr != res_line.reslinnr)))).first()

            if not rline:
                guest.aufenthalte = guest.aufenthalte + 1

            res_line1 = db_session.query(Res_line1).first()

            guest = db_session.query(Guest).first()

        if real_guest:
            get_output(create_historybl(resnr, reslinnr, res_line.zinr, "checkout", user_init, ""))

        for resline in db_session.query(Resline).filter(
                (Resline.resnr == resnr) &  (Resline.l_zuordnung[2] == 1) &  (Resline.kontakt_nr == reslinnr) &  (Resline.active_flag <= 1)).all():

            if real_guest:
                resline.active_flag = 2
                resline.resstatus = 8
                resline.abreise = co_date
                resline.abreisezeit = get_current_time_in_seconds()
                resline.changed = co_date
                resline.changed_id = user_init

        for bill1 in db_session.query(Bill1).filter(
                (Bill1.resnr == resnr) &  (Bill1.parent_nr == reslinnr) &  (Bill1.flag == 0)).all():
            bill1.vesrcod = user_init
            bill1.flag = 1
            bill1.datum = co_date


            bl_saldo = 0

            for bill_line in db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == bill1.rechnr)).all():
                bl_saldo = bl_saldo + bill_line.betrag

            if bl_saldo != bill1.saldo:

                tbuff = db_session.query(Tbuff).filter(
                        (Tbuff._recid == bill1._recid)).first()
                tbuff.saldo = bl_saldo

                tbuff = db_session.query(Tbuff).first()


        for bill1 in db_session.query(Bill1).filter(
                (Bill1.resnr == resnr) &  (Bill1.parent_nr == reslinnr) &  (func.lower(Bill1.(zinr).lower()) == (zinr).lower())).all():

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

            res_line2 = db_session.query(Res_line2).filter(
                    (Res_line2.resnr == res_line.resnr) &  (Res_line2.active_flag < 2)).first()

            if not res_line2:

                reservation = db_session.query(Reservation).first()
                reservation.activeflag = 1

                reservation = db_session.query(Reservation).first()

            if tot_umsatz != 0:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == bill1.gastnr)).first()
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
                guest.aufenthalte = guest.aufenthalte + 1
                guest.resflag = 0

                guest = db_session.query(Guest).first()

                if res_line.gastnrmember != res_line.gastnr:
                    get_min_reslinnr()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnr)).first()
                    guest.zimmeranz = guest.zimmeranz + 1

                    if min_reslinnr == 1:
                        guest.aufenthalte = guest.aufenthalte + 1

                    guest = db_session.query(Guest).first()

                res_line = db_session.query(Res_line).first()
            else:
                res_line.cancelled = co_date

                res_line = db_session.query(Res_line).first()

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

                    mealcoup = db_session.query(Mealcoup).first()
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

                master = db_session.query(Master).first()
                master.active = False

                master = db_session.query(Master).first()


                bill1 = db_session.query(Bill1).filter(
                        (Bill1.resnr == resnr) &  (Bill1.reslinnr == 0)).first()

                if bill1.rechnr != 0:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == bill1.gastnr)).first()

                    if guest:

                        guest = db_session.query(Guest).first()
                        guest.logisumsatz = guest.logisumsatz + bill1.logisumsatz
                        guest.argtumsatz = guest.argtumsatz + bill1.argtumsatz
                        guest.f_b_umsatz = guest.f_b_umsatz + bill1.f_b_umsatz
                        guest.sonst_umsatz = guest.sonst_umsatz + bill1.sonst_umsatz
                        guest.gesamtumsatz = guest.gesamtumsatz + bill1.gesamtumsatz

                        guest = db_session.query(Guest).first()


            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 24) &  (func.lower(Queasy.char1) == (zinr).lower())).all():
                db_session.delete(queasy)


        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "flag") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.reslinnr == reslinnr) &  (Reslin_queasy.betriebsnr == 0)).first()

        if reslin_queasy:
            db_session.delete(reslin_queasy)
        checked_out = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1002)).first()

        if htparam.flogical:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 1099)).first()

            if htparam.paramgruppe == 27 and htparam.flogical:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()

                if guest.email_adr != "":
                    pass
        msg_str = msg_str + chr(2) + "&M" + translateExtended ("Guest checked_out.", lvcarea, "") + chr(10)

        mbill = db_session.query(Mbill).filter(
                (Mbill.resnr == resnr) &  (Mbill.zinr == "")).first()

        if not mbill:

            return

        resline = db_session.query(Resline).filter(
                (Resline.resnr == resnr) &  (Resline.active_flag <= 1)).first()

        if not resline:
            msg_str = msg_str + chr(2) + translateExtended ("All guests checked_out, close the master bill SOONEST", lvcarea, "") + chr(10) + translateExtended ("BillNo : ", lvcarea, "") + to_string(mbill.rechnr) + " - " + translateExtended ("ResNo : ", lvcarea, "") + to_string(mbill.resnr) + chr(10)

    def get_min_reslinnr():

        nonlocal co_ok, checked_out, flag_report, msg_str, co_date, min_reslinnr, real_guest, main_guest, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, bediener, htparam, bill, reservation, res_line, reslin_queasy, guest, arrangement, bill_line, zimmer, res_history, outorder, guestat, akt_cust, salestat, zimplan, resplan, mealcoup, queasy, master
        nonlocal usr1, tbuff, bill1, res_line1, res_line2, rline, resline, sharer, rguest, mbill


        nonlocal usr1, tbuff, bill1, res_line1, res_line2, rline, resline, sharer, rguest, mbill


        Resline = Res_line

        for resline in db_session.query(Resline).filter(
                (Resline.resnr == resnr) &  (Resline.active_flag == 1) &  (Resline.resstatus != 12)).all():
            min_reslinnr = min_reslinnr + 1


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 974)).first()
    unbalanced_bill = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    co_date = htparam.fdate

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    if case_type == 1:
        check_billstatus()

    elif case_type == 2:
        guest_checkout()

    return generate_output()