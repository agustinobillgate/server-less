#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 211/7/2025
# tambah if is None return
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.intevent_1 import intevent_1
from functions.create_historybl import create_historybl
from models import Bediener, Htparam, Bill, Res_line, Reservation, Reslin_queasy, Guest, Bill_line, Arrangement, Zimmer, Res_history, Outorder, Guestat, Akt_cust, Salestat, Zimplan, Resplan, Mealcoup, Queasy, Master, Zimkateg

def res_checkoutbl(pvilanguage:int, case_type:int, resnr:int, reslinnr:int, silenzio:bool, user_init:string):

    prepare_cache ([Bediener, Htparam, Bill, Res_line, Reservation, Guest, Arrangement, Zimmer, Res_history, Guestat, Akt_cust, Salestat, Resplan, Mealcoup, Queasy, Master, Zimkateg])

    co_ok = True
    checked_out = False
    flag_report = False
    msg_str = ""
    co_date:date = None
    min_reslinnr:int = 0
    real_guest:bool = True
    main_guest:bool = False
    unbalanced_bill:bool = False
    priscilla_active:bool = True
    co_ankunft_int:int = 0
    abreise_date:date = None
    lvcarea:string = "res-checkout"
    bl_saldo:Decimal = to_decimal("0.0")
    bediener = htparam = bill = res_line = reservation = reslin_queasy = guest = bill_line = arrangement = zimmer = res_history = outorder = guestat = akt_cust = salestat = zimplan = resplan = mealcoup = queasy = master = zimkateg = None

    usr1 = tbuff = buf_rline = None

    Usr1 = create_buffer("Usr1",Bediener)
    Tbuff = create_buffer("Tbuff",Bill)
    Buf_rline = create_buffer("Buf_rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal co_ok, checked_out, flag_report, msg_str, co_date, min_reslinnr, real_guest, main_guest, unbalanced_bill, priscilla_active, co_ankunft_int, abreise_date, lvcarea, bl_saldo, bediener, htparam, bill, res_line, reservation, reslin_queasy, guest, bill_line, arrangement, zimmer, res_history, outorder, guestat, akt_cust, salestat, zimplan, resplan, mealcoup, queasy, master, zimkateg
        nonlocal pvilanguage, case_type, resnr, reslinnr, silenzio, user_init
        nonlocal usr1, tbuff, buf_rline


        nonlocal usr1, tbuff, buf_rline

        return {"co_ok": co_ok, "checked_out": checked_out, "flag_report": flag_report, "msg_str": msg_str}

    def check_billstatus():

        nonlocal co_ok, checked_out, flag_report, msg_str, co_date, min_reslinnr, real_guest, main_guest, unbalanced_bill, priscilla_active, co_ankunft_int, abreise_date, lvcarea, bl_saldo, bediener, htparam, bill, res_line, reservation, reslin_queasy, guest, bill_line, arrangement, zimmer, res_history, outorder, guestat, akt_cust, salestat, zimplan, resplan, mealcoup, queasy, master, zimkateg
        nonlocal pvilanguage, case_type, resnr, reslinnr, silenzio, user_init
        nonlocal usr1, tbuff, buf_rline


        nonlocal usr1, tbuff, buf_rline

        parent_nr:int = 0
        co_str:string = ""
        bill1 = None
        mbill = None
        resline = None
        rline = None
        rguest = None
        Bill1 =  create_buffer("Bill1",Bill)
        Mbill =  create_buffer("Mbill",Bill)
        Resline =  create_buffer("Resline",Res_line)
        Rline =  create_buffer("Rline",Res_line)
        Rguest =  create_buffer("Rguest",Guest)

        if unbalanced_bill == False:

            bill1 = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"flag": [(eq, 0)]})

            if bill1:
                parent_nr = bill1.parent_nr

                for bill1 in db_session.query(Bill1).filter(
                         (Bill1.resnr == resnr) & (Bill1.parent_nr == parent_nr) & (Bill1.flag == 0)).order_by(Bill1._recid).all():

                    bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill1.rechnr)]})

                    if bill_line and co_ok and (bill1.rgdruck == 0 or bill1.saldo != 0):
                        co_ok = False

                        if bill1.saldo != 0:
                            msg_str = translateExtended ("RoomNo", lvcarea, "") +\
                                " " + res_line.zinr + " - " +\
                                translateExtended ("BillNo", lvcarea, "") +\
                                " " + to_string(bill1.rechnr) +\
                                " " + translateExtended ("not yet balanced", lvcarea, "") + chr_unicode(10) +\
                                translateExtended ("Check-out not possible.", lvcarea, "")


                        else:
                            msg_str = translateExtended ("RoomNo", lvcarea, "") +\
                                " " + res_line.zinr + " - " +\
                                translateExtended ("BillNo", lvcarea, "") +\
                                " " + to_string(bill1.rechnr) +\
                                " " + translateExtended ("not yet printed", lvcarea, "") + chr_unicode(10) +\
                                translateExtended ("Check-out not possible.", lvcarea, "")

            if not co_ok:

                return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})

        if htparam and htparam.fchar != "":

            resline = get_cache (Res_line, {"resnr": [(eq, resnr)],"active_flag": [(eq, 1)],"resstatus": [(ne, 12)],"reslinnr": [(ne, reslinnr)]})

            if not resline:

                mbill = get_cache (Bill, {"resnr": [(eq, resnr)],"zinr": [(eq, "")],"flag": [(eq, 0)]})

                if mbill and mbill.saldo > 0:

                    rguest = get_cache (Guest, {"gastnr": [(eq, mbill.gastnr)]})

                    if rguest and rguest.zahlungsart == 0:
                        co_ok = False
                        msg_str = translateExtended ("RoomNo", lvcarea, "") +\
                                " " + res_line.zinr + " - " +\
                                translateExtended ("Master Bill not yet settled.", lvcarea, "") + chr_unicode(10) +\
                                translateExtended ("Check-out not possible.", lvcarea, "") + chr_unicode(10)

                        return

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if res_line.abreise > co_date:
            co_ok = substring(bediener.permissions, 69, 1) >= "2"
            co_str = translateExtended ("EARLY Check-out", lvcarea, "")
        else:
            co_ok = True
            co_str = translateExtended ("Check-out", lvcarea, "")

        if not silenzio and co_ok:
            msg_str = "&Q" + co_str + " " + res_line.name + chr_unicode(10) + translateExtended ("ROOM", lvcarea, "") + " " + res_line.zinr + " ?"

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "flag")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"betriebsnr": [(eq, 0)]})

            if reslin_queasy and (reslin_queasy.logi1  or reslin_queasy.logi2  or reslin_queasy.logi3 ):
                flag_report = True


    def guest_checkout():

        nonlocal co_ok, checked_out, flag_report, msg_str, co_date, min_reslinnr, real_guest, main_guest, unbalanced_bill, priscilla_active, co_ankunft_int, abreise_date, lvcarea, bl_saldo, bediener, htparam, bill, res_line, reservation, reslin_queasy, guest, bill_line, arrangement, zimmer, res_history, outorder, guestat, akt_cust, salestat, zimplan, resplan, mealcoup, queasy, master, zimkateg
        nonlocal pvilanguage, case_type, resnr, reslinnr, silenzio, user_init
        nonlocal usr1, tbuff, buf_rline


        nonlocal usr1, tbuff, buf_rline

        ankunft:date = None
        abreise:date = None
        resstatus:int = 0
        res_recid:int = 0
        res_recid1:int = 0
        tot_umsatz:Decimal = to_decimal("0.0")
        day_use:bool = False
        dummy_logi:bool = False
        pax:int = 0
        zinr:string = ""
        bill_date:date = None
        bill1 = None
        res_line1 = None
        res_line2 = None
        rline = None
        resline = None
        sharer = None
        rguest = None
        mbill = None
        Bill1 =  create_buffer("Bill1",Bill)
        Res_line1 =  create_buffer("Res_line1",Res_line)
        Res_line2 =  create_buffer("Res_line2",Res_line)
        Rline =  create_buffer("Rline",Res_line)
        Resline =  create_buffer("Resline",Res_line)
        Sharer =  create_buffer("Sharer",Res_line)
        Rguest =  create_buffer("Rguest",Guest)
        Mbill =  create_buffer("Mbill",Bill)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate
        zinr = res_line.zinr
        pax = res_line.erwachs
        main_guest = (res_line.resstatus == 6)

        if main_guest and (res_line.abreise > co_date) and not silenzio:

            sharer = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"zinr": [(eq, res_line.zinr)],"resstatus": [(eq, 13)],"abreise": [(gt, co_date)],"zipreis": [(eq, 0)]})

            if sharer:
                msg_str = "&W" + translateExtended ("Room sharer found with ZERO rate for room", lvcarea, "") + " " + res_line.zinr + chr_unicode(10) + translateExtended ("Change room sharer status and update the Rate.", lvcarea, "") + chr_unicode(10)

        if co_date == res_line.ankunft:

            if res_line.l_zuordnung[2] == 1:
                real_guest = False
            else:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, bill_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
                real_guest = None != bill_line

        htparam = get_cache (Htparam, {"paramnr": [(eq, 307)]})

        if htparam.flogical:
            get_output(intevent_1(2, res_line.zinr, "My Checkout!", res_line.resnr, res_line.reslinnr))

        if priscilla_active:
            get_output(intevent_1(2, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})

        if zimmer:

            usr1 = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if usr1:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usr1.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "C/O " + "Room " + zimmer.zinr + " Status Changed From " + to_string(zimmer.zistatus) + " to Vacant Dirty"
                res_history.action = "FO Cashier"


                pass
                pass

            res_line1 = db_session.query(Res_line1).filter(
                     (Res_line1._recid != res_line._recid) & (Res_line1.zinr == (zinr).lower()) & ((Res_line1.resstatus == 6) | (Res_line1.resstatus == 13)) & (Res_line1.l_zuordnung[inc_value(2)] == 0)).first()

            if not res_line1:

                outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespstart": [(le, co_date)],"gespende": [(ge, co_date)],"betriebsnr": [(le, 1)]})
                
                db_session.refresh(zimmer, with_for_update=True)

                if not outorder:
                    zimmer.zistatus = 2
                    zimmer.bediener_nr_stat = 0


                else:
                    zimmer.zistatus = 6
                    zimmer.bediener_nr_stat = 0


                pass

        for bill1 in db_session.query(Bill1).filter(
                 (Bill1.resnr == resnr) & (Bill1.parent_nr == reslinnr) & (Bill1.flag == 0) & (Bill1.zinr == res_line.zinr)).order_by(Bill1._recid).all():
            tot_umsatz =  to_decimal(tot_umsatz) + to_decimal(bill1.gesamtumsatz)

        bill1 = get_cache (Bill, {"resnr": [(eq, resnr)],"parent_nr": [(eq, reslinnr)],"zinr": [(eq, res_line.zinr)]})

        if not bill1:

            res_line1 = db_session.query(Res_line1).filter(
                     (Res_line1._recid == res_line._recid)).with_for_update().first()
            res_line1.resstatus = 8
            res_line1.abreise = co_date
            res_line1.abreisezeit = get_current_time_in_seconds()
            res_line1.changed = co_date
            res_line1.changed_id = user_init
            res_line1.active_flag = 2

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line1.gastnrmember)).with_for_update().first()
            guest.date1 = res_line1.ankunft
            guest.date2 = res_line1.abreise
            guest.zimmeranz = guest.zimmeranz + 1
            guest.resflag = 0

            rline = db_session.query(Rline).filter(
                     (Rline.resstatus == 8) & (Rline.abreise == co_date) & (Rline.gastnrmember == guest.gastnr) & (((Rline.resnr != res_line.resnr)) | ((Rline.reslinnr != res_line.reslinnr)))).first()

            if not rline:
                guest.aufenthalte = guest.aufenthalte + 1


            pass
            pass

        if real_guest:
            get_output(create_historybl(resnr, reslinnr, res_line.zinr, "checkout", user_init, ""))

        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == resnr) & (Resline.l_zuordnung[inc_value(2)] == 1) & (Resline.kontakt_nr == reslinnr) & (Resline.active_flag <= 1)).order_by(Resline._recid).all():

            if real_guest:
                resline.active_flag = 2
                resline.resstatus = 8
                resline.abreise = co_date
                resline.abreisezeit = get_current_time_in_seconds()
                resline.changed = co_date
                resline.changed_id = user_init

        for bill1 in db_session.query(Bill1).filter(
                 (Bill1.resnr == resnr) & (Bill1.parent_nr == reslinnr) & (Bill1.flag == 0)).with_for_update().order_by(Bill1._recid).all():
            bill1.vesrcod = user_init
            bill1.flag = 1
            bill1.datum = co_date


            bl_saldo =  to_decimal("0")

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill1.rechnr)).order_by(Bill_line._recid).all():
                bl_saldo =  to_decimal(bl_saldo) + to_decimal(bill_line.betrag)

            if bl_saldo != bill1.saldo:

                tbuff = db_session.query(Tbuff).filter(
                         (Tbuff._recid == bill1._recid)).with_for_update().first()
                tbuff.saldo =  to_decimal(bl_saldo)
                pass
                pass

        for bill1 in db_session.query(Bill1).filter(
                 (Bill1.resnr == resnr) & (Bill1.parent_nr == reslinnr) & (Bill1.zinr == (zinr).lower())).with_for_update().order_by(Bill1._recid).all():

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == bill1.resnr) & (Res_line.reslinnr == bill1.reslinnr) & (Res_line.zinr == (bill1.zinr).lower())).with_for_update().first()

            if res_line:
                db_session.refresh(res_line, with_for_update=True)

                res_recid = res_line._recid
                resstatus = res_line.resstatus
                ankunft = res_line.ankunft
                abreise = res_line.abreise

                if res_line.resstatus != 12:
                    res_line.resstatus = 8

                res_line.abreise = co_date
                abreise_date = res_line.abreise

                res_line.abreisezeit = get_current_time_in_seconds()
                res_line.changed = co_date
                res_line.changed_id = user_init
                res_line.active_flag = 2

                res_line2 = db_session.query(Res_line2).filter(
                         (Res_line2.resnr == res_line.resnr) & (Res_line2.active_flag < 2)).first()

                if not res_line2:
                    db_session.refresh(reservation, with_for_update=True)
                    reservation.activeflag = 1

            if tot_umsatz != 0:
                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == bill1.gastnr)).with_for_update().first()


                guest.logisumsatz =  to_decimal(guest.logisumsatz) + to_decimal(bill1.logisumsatz)
                guest.argtumsatz =  to_decimal(guest.argtumsatz) + to_decimal(bill1.argtumsatz)
                guest.f_b_umsatz =  to_decimal(guest.f_b_umsatz) + to_decimal(bill1.f_b_umsatz)
                guest.sonst_umsatz =  to_decimal(guest.sonst_umsatz) + to_decimal(bill1.sonst_umsatz)
                guest.gesamtumsatz =  to_decimal(guest.gesamtumsatz) + to_decimal(bill1.gesamtumsatz)
                

                guestat = db_session.query(Guestat).filter(
                         (Guestat.gastnr == res_line.gastnr) & (Guestat.monat == get_month(bill_date)) & (Guestat.jahr == get_year(bill_date)) & (Guestat.betriebsnr == 0)).with_for_update().first()

                if not guestat:
                    guestat = Guestat()
                    db_session.add(guestat)

                    guestat.gastnr = res_line.gastnr
                    guestat.monat = get_month(bill_date)
                    guestat.jahr = get_year(bill_date)


                guestat.logisumsatz =  to_decimal(guestat.logisumsatz) + to_decimal(bill1.logisumsatz)
                guestat.argtumsatz =  to_decimal(guestat.argtumsatz) + to_decimal(bill1.argtumsatz)
                guestat.f_b_umsatz =  to_decimal(guestat.f_b_umsatz) + to_decimal(bill1.f_b_umsatz)
                guestat.sonst_umsatz =  to_decimal(guestat.sonst_umsatz) + to_decimal(bill1.sonst_umsatz)
                guestat.gesamtumsatz =  to_decimal(guestat.gesamtumsatz) + to_decimal(bill1.gesamtumsatz)


                pass

                akt_cust = get_cache (Akt_cust, {"gastnr": [(eq, res_line.gastnr)]})

                if akt_cust:

                    bediener = get_cache (Bediener, {"userinit": [(eq, akt_cust.userinit)]})

                if not akt_cust or not bediener:

                    rguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    if rguest.phonetik3 != "":

                        bediener = get_cache (Bediener, {"userinit": [(eq, rguest.phonetik3)]})

                if bediener:

                    salestat = db_session.query(Salestat).filter(
                             (Salestat.bediener_nr == bediener.nr) & (Salestat.jahr == get_year(bill_date)) & (Salestat.monat == get_month(bill_date))).with_for_update().first()

                    if not salestat:
                        salestat = Salestat()
                        db_session.add(salestat)

                        salestat.bediener_nr = bediener.nr
                        salestat.jahr = get_year(bill_date)
                        salestat.monat = get_month(bill_date)


                    salestat.logisumsatz =  to_decimal(salestat.logisumsatz) + to_decimal(bill1.logisumsatz)
                    salestat.argtumsatz =  to_decimal(salestat.argtumsatz) + to_decimal(bill1.argtumsatz)
                    salestat.f_b_umsatz =  to_decimal(salestat.f_b_umsatz) + to_decimal(bill1.f_b_umsatz)
                    salestat.sonst_umsatz =  to_decimal(salestat.sonst_umsatz) + to_decimal(bill1.sonst_umsatz)
                    salestat.gesamtumsatz =  to_decimal(salestat.gesamtumsatz) + to_decimal(bill1.gesamtumsatz)

                    if res_line.resstatus != 12:
                        co_ankunft_int = (co_date - ankunft).days


                        salestat.room_nights = salestat.room_nights + co_ankunft_int

                        if co_ankunft_int == 0:
                            salestat.room_nights = salestat.room_nights + 1
                    pass

            if real_guest and res_line.resstatus != 12:

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnrmember)).with_for_update().first()
                guest.date1 = res_line.ankunft
                guest.date2 = res_line.abreise
                guest.zimmeranz = guest.zimmeranz + 1
                guest.aufenthalte = guest.aufenthalte + 1
                guest.resflag = 0


                pass

                if res_line.gastnrmember != res_line.gastnr:
                    get_min_reslinnr()
                    guest = db_session.query(Guest).filter(
                             (Guest.gastnr == res_line.gastnr)).with_for_update().first()

                    guest.zimmeranz = guest.zimmeranz + 1

                    if min_reslinnr == 1:
                        guest.aufenthalte = guest.aufenthalte + 1
                    pass
                pass
            else:
                res_line.cancelled = co_date
                pass
                pass
            res_recid1 = 0

            for zimplan in db_session.query(Zimplan).filter(
                     (Zimplan.datum >= co_date) & (Zimplan.datum < abreise) & (Zimplan.zinr == zinr) & (Zimplan.res_recid == res_recid)).with_for_update().order_by(Zimplan._recid).all():

                if res_recid1 != 0:

                    if zimplan.datum < res_line1.abreise:
                        zimplan.res_recid = res_recid1
                    else:
                        db_session.delete(zimplan)

            if resstatus != 12:

                for resplan in db_session.query(Resplan).filter(
                         (Resplan.datum >= co_date) & (Resplan.datum < abreise) & (Resplan.zikatnr == zimmer.zikatnr)).with_for_update().order_by(Resplan._recid).all():
                    resplan.anzzim[resstatus - 1] = resplan.anzzim[resstatus - 1] - 1
                    pass

            resline = db_session.query(Resline).filter(
                     (Resline.resnr == resnr) & ((Resline.active_flag == 0) | (Resline.active_flag == 1)) & (Resline.resstatus != 12)).first()

            if not resline:

                mealcoup = db_session.query(Mealcoup).filter(
                         (Mealcoup.zinr == zinr) & (Mealcoup.activeflag == True)).with_for_update().first()

                if mealcoup:
                    pass
                    mealcoup.activeflag = False
                    mealcoup.abreise = get_current_date()
                    pass
                    pass

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 16) & (Queasy.number1 == resnr) & (Queasy.number2 == reslinnr)).with_for_update().order_by(Queasy._recid).all():
                db_session.delete(queasy)
                pass

        res_line1 = db_session.query(Res_line1).filter(
                 ((Res_line1.resnr == resnr)) & ((Res_line1.reslinnr != reslinnr)) & ((Res_line1.resstatus == 6) | (Res_line1.resstatus == 13))).first()

        if not res_line1:

            master = db_session.query(Master).filter(
                     (Master.resnr == resnr)).with_for_update().first()
            
            if master:
                db_session.refresh(master, with_for_update=True)
                master.active = False

                bill1 = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, 0)]})

                if bill1.rechnr != 0:

                    guest = db_session.query(Guest).filter(
                             (Guest.gastnr == bill1.gastnr)).first()

                    if guest:
                        db_session.refresh(guest, with_for_update=True)

                        guest.logisumsatz =  to_decimal(guest.logisumsatz) + to_decimal(bill1.logisumsatz)
                        guest.argtumsatz =  to_decimal(guest.argtumsatz) + to_decimal(bill1.argtumsatz)
                        guest.f_b_umsatz =  to_decimal(guest.f_b_umsatz) + to_decimal(bill1.f_b_umsatz)
                        guest.sonst_umsatz =  to_decimal(guest.sonst_umsatz) + to_decimal(bill1.sonst_umsatz)
                        guest.gesamtumsatz =  to_decimal(guest.gesamtumsatz) + to_decimal(bill1.gesamtumsatz)


                        pass
                        pass

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 24) & (Queasy.char1 == (zinr).lower())).with_for_update().order_by(Queasy._recid).all():
                db_session.delete(queasy)
                pass

        # reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "flag")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"betriebsnr": [(eq, 0)]})
        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == "flag") & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.reslinnr == reslinnr) & (Reslin_queasy.betriebsnr == 0)).with_for_update().first()

        if reslin_queasy:
            db_session.delete(reslin_queasy)

        checked_out = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1002)]})

        if htparam.flogical:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 1099)]})

            if htparam.paramgruppe == 27 and htparam.flogical:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest.email_adr != "":
                    pass
        msg_str = msg_str + chr_unicode(2) + "&M" + translateExtended ("Guest checked-out.", lvcarea, "") + chr_unicode(10)

        mbill = get_cache (Bill, {"resnr": [(eq, resnr)],"zinr": [(eq, "")]})

        if not mbill:

            return

        resline = get_cache (Res_line, {"resnr": [(eq, resnr)],"active_flag": [(le, 1)]})

        if not resline:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("All guests checked-out, close the master bill SOONEST", lvcarea, "") + chr_unicode(10) + translateExtended ("BillNo : ", lvcarea, "") + to_string(mbill.rechnr) + " - " + translateExtended ("ResNo : ", lvcarea, "") + to_string(mbill.resnr) + chr_unicode(10)


    def get_min_reslinnr():

        nonlocal co_ok, checked_out, flag_report, msg_str, co_date, min_reslinnr, real_guest, main_guest, unbalanced_bill, priscilla_active, co_ankunft_int, abreise_date, lvcarea, bl_saldo, bediener, htparam, bill, res_line, reservation, reslin_queasy, guest, bill_line, arrangement, zimmer, res_history, outorder, guestat, akt_cust, salestat, zimplan, resplan, mealcoup, queasy, master, zimkateg
        nonlocal pvilanguage, case_type, resnr, reslinnr, silenzio, user_init
        nonlocal usr1, tbuff, buf_rline


        nonlocal usr1, tbuff, buf_rline

        resline = None
        Resline =  create_buffer("Resline",Res_line)

        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == resnr) & (Resline.active_flag == 1) & (Resline.resstatus != 12)).order_by(Resline._recid).all():
            min_reslinnr = min_reslinnr + 1


    def update_queasy171():

        nonlocal co_ok, checked_out, flag_report, msg_str, co_date, min_reslinnr, real_guest, main_guest, unbalanced_bill, priscilla_active, co_ankunft_int, abreise_date, lvcarea, bl_saldo, bediener, htparam, bill, res_line, reservation, reslin_queasy, guest, bill_line, arrangement, zimmer, res_history, outorder, guestat, akt_cust, salestat, zimplan, resplan, mealcoup, queasy, master, zimkateg
        nonlocal pvilanguage, case_type, resnr, reslinnr, silenzio, user_init
        nonlocal usr1, tbuff, buf_rline


        nonlocal usr1, tbuff, buf_rline

        zbuff = None
        qsy = None
        i:int = 0
        upto_date:date = None
        iftask:string = ""
        origcode:string = ""
        cat_flag:bool = False
        roomnr:int = 0
        datum:date = None
        Zbuff =  create_buffer("Zbuff",Zimkateg)
        Qsy =  create_buffer("Qsy",Queasy)

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if res_line:
            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                if substring(iftask, 0, 10) == ("$origcode$").lower() :
                    origcode = substring(iftask, 10)
                    return

            queasy = get_cache (Queasy, {"key": [(eq, 152)]})

            if queasy:
                cat_flag = True

            zbuff = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

            if zbuff:

                if cat_flag:
                    roomnr = zbuff.typ
                else:
                    roomnr = zbuff.zikatnr

            if res_line.ankunft == co_date:
                upto_date = co_date
            else:

                if abreise_date != None:
                    upto_date = abreise_date - timedelta(days=1)
                else:
                    upto_date = co_date

            for datum in date_range(co_date,upto_date) :

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    qsy = db_session.query(Qsy).filter(
                             (Qsy._recid == queasy._recid)).with_for_update().first

                    if qsy:
                        qsy.logi2 = True
                        pass
                        pass

                if origcode != "":

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:

                        qsy = db_session.query(Qsy).filter(
                                 (Qsy._recid == queasy._recid)).with_for_update().first

                        if qsy:
                            qsy.logi2 = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 974)]})
    unbalanced_bill = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    co_date = htparam.fdate

    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    # Rd 221/7/2025
    # if not available return
    if reservation is None:
        return generate_output()

    if not reservation:
        msg_str = translateExtended ("No reservation found.", lvcarea, "")

        return generate_output()

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if not res_line:
        msg_str = translateExtended ("No reservation member found.", lvcarea, "")

        return generate_output()

    if case_type == 1:
        check_billstatus()

    elif case_type == 2:
        guest_checkout()
    update_queasy171()

    buf_rline = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if buf_rline:
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = buf_rline.resnr
        reslin_queasy.reslinnr = buf_rline.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(buf_rline.name) + ";" + to_string("CHECKED-OUT") + ";" + to_string(" ") + ";" + to_string(" ") + ";"
        pass
        pass

    return generate_output()