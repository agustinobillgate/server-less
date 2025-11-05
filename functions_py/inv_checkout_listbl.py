#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 05/11/2025
# bediener.perm diganti bediener.permissions
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.create_historybl import create_historybl
from functions.intevent_1 import intevent_1
from models import Res_line, Bill, Guest, Bediener, Reservation, Htparam, Outorder, Reslin_queasy, Bill_line, Zimmer, Guestat, Akt_cust, Salestat, Res_history, Zimplan, Resplan, Mealcoup, Queasy, Interface, Master, Zimkateg

def inv_checkout_listbl(pvilanguage:int, case_type:int, resnr:int, reslinnr:int, user_init:string, reason_str:string, silenzio:bool):

    prepare_cache ([Res_line, Bill, Guest, Bediener, Reservation, Htparam, Outorder, Reslin_queasy, Bill_line, Zimmer, Guestat, Akt_cust, Salestat, Res_history, Resplan, Mealcoup, Queasy, Interface, Master, Zimkateg])

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
    abreise_date:date = None
    zinr:string = ""
    add_str:string = ""
    main_guest:bool = False
    co_ok:bool = False
    zugriff:bool = False
    answer:bool = True
    room_added:bool = False
    do_it:bool = False
    statusstr:string = ""
    unbalanced_bill:bool = False
    priscilla_active:bool = True
    lvcarea:string = "inv-checkout-listbl"
    bl_saldo:Decimal = to_decimal("0.0")
    res_line = bill = guest = bediener = reservation = htparam = outorder = reslin_queasy = bill_line = zimmer = guestat = akt_cust = salestat = res_history = zimplan = resplan = mealcoup = queasy = interface = master = zimkateg = None

    resline = mbill = rguest = rline = bline = buf_rline = tbuff = None

    Resline = create_buffer("Resline",Res_line)
    Mbill = create_buffer("Mbill",Bill)
    Rguest = create_buffer("Rguest",Guest)
    Rline = create_buffer("Rline",Res_line)
    Bline = create_buffer("Bline",Bediener)
    Buf_rline = create_buffer("Buf_rline",Res_line)
    Tbuff = create_buffer("Tbuff",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, checked_out, early_co, goto_master, flag_report, msg_str, msg_int, min_reslinnr, pax, rechnr, rm_nite, co_date, bill_date, abreise_date, zinr, add_str, main_guest, co_ok, zugriff, answer, room_added, do_it, statusstr, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, res_line, bill, guest, bediener, reservation, htparam, outorder, reslin_queasy, bill_line, zimmer, guestat, akt_cust, salestat, res_history, zimplan, resplan, mealcoup, queasy, interface, master, zimkateg
        nonlocal pvilanguage, case_type, resnr, reslinnr, user_init, reason_str, silenzio
        nonlocal resline, mbill, rguest, rline, bline, buf_rline, tbuff


        nonlocal resline, mbill, rguest, rline, bline, buf_rline, tbuff

        return {"error_code": error_code, "checked_out": checked_out, "early_co": early_co, "goto_master": goto_master, "flag_report": flag_report, "msg_str": msg_str, "msg_int": msg_int}

    def check_billstatus():

        nonlocal error_code, checked_out, early_co, goto_master, flag_report, msg_str, msg_int, min_reslinnr, pax, rechnr, rm_nite, co_date, bill_date, abreise_date, zinr, add_str, main_guest, co_ok, zugriff, answer, room_added, do_it, statusstr, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, res_line, bill, guest, bediener, reservation, htparam, outorder, reslin_queasy, bill_line, zimmer, guestat, akt_cust, salestat, res_history, zimplan, resplan, mealcoup, queasy, interface, master, zimkateg
        nonlocal pvilanguage, case_type, resnr, reslinnr, user_init, reason_str, silenzio
        nonlocal resline, mbill, rguest, rline, bline, buf_rline, tbuff


        nonlocal resline, mbill, rguest, rline, bline, buf_rline, tbuff

        co_ok = True
        parent_nr:int = 0
        bill1 = None

        def generate_inner_output():
            return (co_ok)

        Bill1 =  create_buffer("Bill1",Bill)

        if unbalanced_bill == False:

            bill1 = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"flag": [(eq, 0)],"zinr": [(eq, zinr)]})

            if bill1:
                parent_nr = bill1.parent_nr

                for bill1 in db_session.query(Bill1).filter(
                         (Bill1.resnr == resnr) & (Bill1.parent_nr == parent_nr) & (Bill1.flag == 0)).order_by(Bill1._recid).all():

                    bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill1.rechnr)]})

                    if bill_line and co_ok and (bill1.rgdruck == 0 or bill1.saldo != 0):
                        co_ok = False
                        rechnr = bill1.rechnr

                        if bill1.saldo != 0:
                            error_code = 1
                            msg_str = translateExtended ("RoomNo", lvcarea, "") +\
                                " " + zinr + " - " +\
                                translateExtended ("BillNo", lvcarea, "") +\
                                " " + to_string(rechnr) + " " +\
                                translateExtended ("not yet balanced", lvcarea, "") + chr_unicode(10) +\
                                translateExtended ("Check-out not possible.", lvcarea, "") + chr_unicode(10)


                        else:
                            error_code = 2
                            msg_str = translateExtended ("RoomNo", lvcarea, "") +\
                                " " + zinr + " - " +\
                                translateExtended ("BillNo", lvcarea, "") +\
                                " " + to_string(rechnr) + " " +\
                                translateExtended ("not yet printed.", lvcarea, "") + chr_unicode(10) +\
                                translateExtended ("Check-out not possible.", lvcarea, "") + chr_unicode(10)

                        return generate_inner_output()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})

        if htparam.fchar != "":

            resline = get_cache (Res_line, {"resnr": [(eq, resnr)],"active_flag": [(eq, 1)],"resstatus": [(ne, 12)],"reslinnr": [(ne, reslinnr)]})

            if not resline:

                mbill = get_cache (Bill, {"resnr": [(eq, resnr)],"zinr": [(eq, "")],"flag": [(eq, 0)]})

                if mbill and mbill.saldo > 0:

                    rguest = get_cache (Guest, {"gastnr": [(eq, mbill.gastnr)]})

                    if rguest.zahlungsart == 0:
                        error_code = 3
                        co_ok = False
                        msg_str = translateExtended ("RoomNo", lvcarea, "") +\
                            " " + zinr + " - " +\
                            translateExtended ("Master Bill not yet settled.", lvcarea, "") + chr_unicode(10) +\
                            translateExtended ("Check-out not possible.", lvcarea, "") + chr_unicode(10)

        return generate_inner_output()


    def check_co_time():

        nonlocal error_code, checked_out, early_co, goto_master, flag_report, msg_str, msg_int, min_reslinnr, pax, rechnr, rm_nite, co_date, bill_date, abreise_date, zinr, add_str, main_guest, co_ok, zugriff, answer, room_added, do_it, statusstr, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, res_line, bill, guest, bediener, reservation, htparam, outorder, reslin_queasy, bill_line, zimmer, guestat, akt_cust, salestat, res_history, zimplan, resplan, mealcoup, queasy, interface, master, zimkateg
        nonlocal pvilanguage, case_type, resnr, reslinnr, user_init, reason_str, silenzio
        nonlocal resline, mbill, rguest, rline, bline, buf_rline, tbuff


        nonlocal resline, mbill, rguest, rline, bline, buf_rline, tbuff

        co_zeit:int = 0
        co_datum:date = None
        zeit:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1076)]})

        if htparam.feldtyp == 4 and htparam.flogical:
            co_zeit = res_line.abreisezeit

            if co_zeit == 0:
                co_zeit = 12 * 3600
            co_datum = res_line.abreise
            zeit = get_current_time_in_seconds()

            if (co_datum == bill_date) and (zeit > co_zeit):
                msg_int = 4
                msg_str = translateExtended ("C/O Time", lvcarea, "") + " " + to_string(co_zeit, "HH:MM:SS") + " " + translateExtended ("exceeded. Current time is", lvcarea, "") + " " + to_string(zeit, "HH:MM:SS") + chr_unicode(10) + translateExtended ("Exceeded time =", lvcarea, "") + " " + to_string((zeit - co_zeit) , "HH:MM:SS") + chr_unicode(10)


    def guest_checkout():

        nonlocal error_code, checked_out, early_co, goto_master, flag_report, msg_str, msg_int, min_reslinnr, pax, rechnr, rm_nite, co_date, bill_date, abreise_date, zinr, add_str, main_guest, co_ok, zugriff, answer, room_added, do_it, statusstr, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, res_line, bill, guest, bediener, reservation, htparam, outorder, reslin_queasy, bill_line, zimmer, guestat, akt_cust, salestat, res_history, zimplan, resplan, mealcoup, queasy, interface, master, zimkateg
        nonlocal pvilanguage, case_type, resnr, reslinnr, user_init, reason_str, silenzio
        nonlocal resline, mbill, rguest, rline, bline, buf_rline, tbuff


        nonlocal resline, mbill, rguest, rline, bline, buf_rline, tbuff

        bill1 = None
        rline = None
        res_line1 = None
        res_line2 = None
        sharer = None
        ankunft:date = None
        abreise:date = None
        resstatus:int = 0
        res_recid:int = 0
        res_recid1:int = 0
        tot_umsatz:Decimal = to_decimal("0.0")
        day_use:bool = False
        real_guest:bool = True
        sales_lic:bool = False
        dummy_logi:bool = False
        sharer_co:bool = False
        avail_bill_line:int = 0
        Bill1 =  create_buffer("Bill1",Bill)
        Rline =  create_buffer("Rline",Res_line)
        Res_line1 =  create_buffer("Res_line1",Res_line)
        Res_line2 =  create_buffer("Res_line2",Res_line)
        Sharer =  create_buffer("Sharer",Res_line)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "flag")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"betriebsnr": [(eq, 0)]})

        if reslin_queasy and (reslin_queasy.logi1  or reslin_queasy.logi2  or reslin_queasy.logi3 ):
            flag_report = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1002)]})
        sales_lic = htparam.flogical

        if res_line.betrieb_gast > 0:
            msg_int = 5
            msg_str = translateExtended ("Number of created KeyCard(s) =", lvcarea, "") + " " + to_string(res_line.betrieb_gast) + chr_unicode(10)

        zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})

        res_line1 = db_session.query(Res_line1).filter(
                 (Res_line1._recid != res_line._recid) & (Res_line1.zinr == (zinr))) & ((Res_line1.resstatus == 6) | (Res_line1.resstatus == 13)) & (Res_line1.l_zuordnung[inc_value(2)] == 0).first()

        if not res_line1:

            outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespstart": [(le, co_date)],"gespende": [(ge, co_date)],"betriebsnr": [(le, 1)]})
            pass

            if outorder:
                zimmer.zistatus = 6
                zimmer.bediener_nr_stat = 0


            else:
                zimmer.zistatus = 2
                zimmer.bediener_nr_stat = 0


            pass
            pass

        for bill1 in db_session.query(Bill1).filter(
                 (Bill1.resnr == resnr) & (Bill1.parent_nr == reslinnr) & (Bill1.flag == 0) & (Bill1.zinr == (zinr))).order_by(Bill1._recid).all():
            tot_umsatz =  to_decimal(tot_umsatz) + to_decimal(bill1.gesamtumsatz)

        if (co_date - res_line.ankunft) == 0 and tot_umsatz == 0:
            real_guest = False

        for sharer in db_session.query(Sharer).filter(
                     (Sharer.resnr == resnr) & (Sharer.kontakt_nr == reslinnr) & (Sharer.l_zuordnung[inc_value(2)] == 1) & (Sharer.active_flag <= 1)).order_by(Sharer._recid).all():

            if real_guest:
                get_output(create_historybl(sharer.resnr, sharer.reslinnr, sharer.zinr, "checkout", user_init, ""))
            sharer.active_flag = 2
            sharer.resstatus = 8
            sharer.abreise = co_date
            sharer.abreisezeit = get_current_time_in_seconds()
            sharer.changed = co_date
            sharer.changed_id = user_init

        htparam = get_cache (Htparam, {"paramnr": [(eq, 307)]})

        if htparam.flogical:
            get_output(intevent_1(2, zinr, "My Checkout!", res_line.resnr, res_line.reslinnr))
        get_output(intevent_1(2, zinr, "bridge", res_line.resnr, res_line.reslinnr))

        if priscilla_active:
            get_output(intevent_1(2, zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        for bill1 in db_session.query(Bill1).filter(
                     (Bill1.resnr == resnr) & (Bill1.parent_nr == reslinnr) & (Bill1.flag == 0)).order_by(Bill1._recid).all():
            bl_saldo =  to_decimal("0")

            for bill_line in db_session.query(Bill_line).filter(
                         (Bill_line.rechnr == bill1.rechnr)).order_by(Bill_line._recid).all():
                bl_saldo =  to_decimal(bl_saldo) + to_decimal(bill_line.betrag)

            if bl_saldo != bill1.saldo:

                tbuff = get_cache (Bill, {"_recid": [(eq, bill1._recid)]})
                tbuff.saldo =  to_decimal(bl_saldo)
                pass
                pass
            bill1.vesrcod = user_init
            bill1.flag = 1
            bill1.datum = co_date

        for bill1 in db_session.query(Bill1).filter(
                     (Bill1.resnr == resnr) & (Bill1.parent_nr == reslinnr) & (Bill1.zinr == (zinr))).order_by(Bill1._recid).all():

            if real_guest and resstatus != 12:
                get_output(create_historybl(resnr, reslinnr, zinr, "checkout", user_init, ""))

            res_line = get_cache (Res_line, {"resnr": [(eq, bill1.resnr)],"reslinnr": [(eq, bill1.reslinnr)],"zinr": [(eq, bill1.zinr)]})
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

            if res_line.erwachs > 0:
                avail_bill_line = bill1.rechnr

            if reason_str != "" and reason_str != None:
                res_line.zimmer_wunsch = res_line.zimmer_wunsch + "earlyCO," + reason_str + ";"

            res_line2 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"active_flag": [(lt, 2)]})

            if not res_line2:
                pass
                reservation.activeflag = 1
                pass

            if tot_umsatz != 0:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                guest.logisumsatz =  to_decimal(guest.logisumsatz) + to_decimal(bill1.logisumsatz)
                guest.argtumsatz =  to_decimal(guest.argtumsatz) + to_decimal(bill1.argtumsatz)
                guest.f_b_umsatz =  to_decimal(guest.f_b_umsatz) + to_decimal(bill1.f_b_umsatz)
                guest.sonst_umsatz =  to_decimal(guest.sonst_umsatz) + to_decimal(bill1.sonst_umsatz)
                guest.gesamtumsatz =  to_decimal(guest.gesamtumsatz) + to_decimal(bill1.gesamtumsatz)


                pass

                guestat = get_cache (Guestat, {"gastnr": [(eq, res_line.gastnr)],"monat": [(eq, get_month(bill_date))],"jahr": [(eq, get_year(bill_date))],"betriebsnr": [(eq, 0)]})

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

                    salestat = get_cache (Salestat, {"bediener_nr": [(eq, bediener.nr)],"jahr": [(eq, get_year(bill_date))],"monat": [(eq, get_month(bill_date))]})

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
                        salestat.room_nights = salestat.room_nights + (co_date - ankunft)

                        if (co_date - ankunft) == 0:
                            salestat.room_nights = salestat.room_nights + 1
                    pass

            if real_guest and res_line.resstatus != 12:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                guest.date1 = res_line.ankunft
                guest.date2 = res_line.abreise
                guest.zimmeranz = guest.zimmeranz + 1
                guest.resflag = 0

                rline = db_session.query(Rline).filter(
                             (Rline.resstatus == 8) & (Rline.abreise == co_date) & (Rline.gastnrmember == guest.gastnr) & (((Rline.resnr != res_line.resnr)) | ((Rline.reslinnr != res_line.reslinnr)))).first()

                if not rline:
                    guest.aufenthalte = guest.aufenthalte + 1


                pass

                if res_line.gastnrmember != res_line.gastnr:
                    get_min_reslinnr()

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                    guest.zimmeranz = guest.zimmeranz + 1

                    if min_reslinnr == 1:
                        guest.aufenthalte = guest.aufenthalte + 1


                    pass

                bline = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bline.nr
                res_history.resnr = res_line.resnr
                res_history.reslinnr = res_line.reslinnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "CheckOut Room " + res_line.zinr +\
                        " ResNo " + to_string(res_line.resnr)
                res_history.action = "CheckOut"


                pass
                pass

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "CheckOut Room " + res_line.zinr +\
                        " ResNo " + to_string(res_line.resnr)
                res_history.action = "CheckOut"


                pass
                pass
                pass
                pass
            else:
                res_line.cancelled = co_date
                pass
            res_recid1 = 0

            for zimplan in db_session.query(Zimplan).filter(
                         (Zimplan.datum >= co_date) & (Zimplan.datum < abreise) & (Zimplan.zinr == (zinr))) & (Zimplan.res_recid == res_recid).order_by(Zimplan._recid).all():

                if res_recid1 != 0:

                    if zimplan.datum < res_line1.abreise:
                        zimplan.res_recid = res_recid1
                    else:
                        db_session.delete(zimplan)

            if resstatus != 12:

                for resplan in db_session.query(Resplan).filter(
                             (Resplan.datum >= co_date) & (Resplan.datum < abreise) & (Resplan.zikatnr == zimmer.zikatnr)).order_by(Resplan._recid).all():
                    resplan.anzzim[resstatus - 1] = resplan.anzzim[resstatus - 1] - 1
                    pass

            resline = db_session.query(Resline).filter(
                         (Resline.resnr == resnr) & ((Resline.active_flag == 0) | (Resline.active_flag == 1)) & (Resline.resstatus != 12)).first()

            if not resline:

                mealcoup = get_cache (Mealcoup, {"zinr": [(eq, zinr)],"activeflag": [(eq, True)]})

                if mealcoup:
                    mealcoup.activeflag = False
                    mealcoup.abreise = get_current_date()
                    pass

            for queasy in db_session.query(Queasy).filter(
                         (Queasy.key == 16) & (Queasy.number1 == resnr) & (Queasy.number2 == reslinnr)).order_by(Queasy._recid).all():
                db_session.delete(queasy)

            if avail_bill_line != 0:
                interface = Interface()
                db_session.add(interface)

                interface.key = 38
                interface.action = True
                interface.nebenstelle = ""
                interface.parameters = "close-bill"
                interface.intfield = bill1.rechnr
                interface.decfield =  to_decimal(bill1.billtyp)
                interface.int_time = get_current_time_in_seconds()
                interface.intdate = get_current_date()
                interface.resnr = bill1.resnr
                interface.reslinnr = bill1.reslinnr


                pass
                pass

        res_line1 = db_session.query(Res_line1).filter(
                     ((Res_line1.resnr == resnr)) & ((Res_line1.reslinnr != reslinnr)) & ((Res_line1.resstatus == 6) | (Res_line1.resstatus == 13))).first()

        if not res_line1:

            master = get_cache (Master, {"resnr": [(eq, resnr)]})

            if master:
                master.active = False
                pass

                bill1 = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, 0)]})

                if bill1 and bill1.rechnr != 0:

                    guest = get_cache (Guest, {"gastnr": [(eq, bill1.gastnr)]})
                    guest.logisumsatz =  to_decimal(guest.logisumsatz) + to_decimal(bill1.logisumsatz)
                    guest.argtumsatz =  to_decimal(guest.argtumsatz) + to_decimal(bill1.argtumsatz)
                    guest.f_b_umsatz =  to_decimal(guest.f_b_umsatz) + to_decimal(bill1.f_b_umsatz)
                    guest.sonst_umsatz =  to_decimal(guest.sonst_umsatz) + to_decimal(bill1.sonst_umsatz)
                    guest.gesamtumsatz =  to_decimal(guest.gesamtumsatz) + to_decimal(bill1.gesamtumsatz)


                    pass

            for queasy in db_session.query(Queasy).filter(
                         (Queasy.key == 24) & (Queasy.char1 == (zinr))).order_by(Queasy._recid).all():
                db_session.delete(queasy)
        checked_out = True
        msg_int = 6
        msg_str = translateExtended ("Guest checked-out.", lvcarea, "") + chr_unicode(10)

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if not silenzio:

            resline = get_cache (Res_line, {"resnr": [(eq, resnr)],"active_flag": [(eq, 1)],"zinr": [(eq, res_line.zinr)],"l_zuordnung[2]": [(eq, 0)],"abreise": [(eq, co_date)]})

            if resline:

                if resline.resstatus == 6:
                    statusstr = translateExtended ("Status: Main Guest; RmRate =", lvcarea, "")
                else:
                    statusstr = translateExtended ("Status: Room Sharer; RmRate =", lvcarea, "")
                    msg_int = 7
                    msg_str = translateExtended ("Other Expected Departure Guest FOUND in the same room:", lvcarea, "") + chr_unicode(10) + resline.name + " " + to_string(resline.ankunft) + " - " + to_string(resline.abreise) + chr_unicode(10) + statusstr + " " + to_string(resline.zipreis)

        mbill = get_cache (Bill, {"resnr": [(eq, resnr)],"zinr": [(eq, "")]})

        if not mbill and res_line.l_zuordnung[4] != 0 and res_line.l_zuordnung[1] == 0:

            mbill = get_cache (Bill, {"resnr": [(eq, res_line.l_zuordnung[4])],"zinr": [(eq, "")],"flag": [(eq, 0)]})

        if mbill:

            resline = get_cache (Res_line, {"resnr": [(eq, mbill.resnr)],"active_flag": [(le, 1)]})

            if not resline:

                if res_line.l_zuordnung[4] == 0:
                    goto_master = True
                else:

                    resline = get_cache (Res_line, {"resnr": [(ne, mbill.resnr)],"active_flag": [(eq, 1)],"l_zuordnung[1]": [(eq, 0)],"l_zuordnung[4]": [(eq, mbill.resnr)]})
                    goto_master = not None != resline

        if goto_master:
            msg_int = 8
            msg_str = translateExtended ("All guests are checked-out, close the master bill NOW?", lvcarea, "") + chr_unicode(10) + translateExtended ("BillNo :", lvcarea, "") + " " + to_string(mbill.rechnr) + " " + translateExtended ("- ResNo :", lvcarea, "") + " " + to_string(mbill.resnr) + chr_unicode(10)


    def get_min_reslinnr():

        nonlocal error_code, checked_out, early_co, goto_master, flag_report, msg_str, msg_int, min_reslinnr, pax, rechnr, rm_nite, co_date, bill_date, abreise_date, zinr, add_str, main_guest, co_ok, zugriff, answer, room_added, do_it, statusstr, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, res_line, bill, guest, bediener, reservation, htparam, outorder, reslin_queasy, bill_line, zimmer, guestat, akt_cust, salestat, res_history, zimplan, resplan, mealcoup, queasy, interface, master, zimkateg
        nonlocal pvilanguage, case_type, resnr, reslinnr, user_init, reason_str, silenzio
        nonlocal resline, mbill, rguest, rline, bline, buf_rline, tbuff


        nonlocal resline, mbill, rguest, rline, bline, buf_rline, tbuff

        resline = None
        Resline =  create_buffer("Resline",Res_line)

        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == resnr) & (Resline.active_flag == 1) & (Resline.resstatus != 12)).order_by(Resline._recid).all():
            min_reslinnr = min_reslinnr + 1


    def update_queasy171():

        nonlocal error_code, checked_out, early_co, goto_master, flag_report, msg_str, msg_int, min_reslinnr, pax, rechnr, rm_nite, co_date, bill_date, abreise_date, zinr, add_str, main_guest, co_ok, zugriff, answer, room_added, do_it, statusstr, unbalanced_bill, priscilla_active, lvcarea, bl_saldo, res_line, bill, guest, bediener, reservation, htparam, outorder, reslin_queasy, bill_line, zimmer, guestat, akt_cust, salestat, res_history, zimplan, resplan, mealcoup, queasy, interface, master, zimkateg
        nonlocal pvilanguage, case_type, resnr, reslinnr, user_init, reason_str, silenzio
        nonlocal resline, mbill, rguest, rline, bline, buf_rline, tbuff


        nonlocal resline, mbill, rguest, rline, bline, buf_rline, tbuff

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

                if substring(iftask, 0, 10) == ("$origCode$") :
                    origcode = substring(iftask, 10).strip()
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
                upto_date = abreise_date - timedelta(days=1)
            for datum in date_range(co_date,upto_date) :

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                    if qsy:
                        qsy.logi2 = True
                        pass
                        pass

                if origcode != "":

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:

                        qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                        if qsy:
                            qsy.logi2 = True
                            pass
                            pass

    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    co_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 974)]})
    unbalanced_bill = htparam.flogical

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
    zinr = res_line.zinr.strip()
    pax = res_line.erwachs
    main_guest = (res_line.resstatus == 6)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})

    if htparam and htparam.fchar != "":

        resline = get_cache (Res_line, {"resnr": [(eq, resnr)],"active_flag": [(eq, 1)],"resstatus": [(ne, 12)],"reslinnr": [(ne, reslinnr)]})

        if not resline:

            mbill = get_cache (Bill, {"resnr": [(eq, resnr)],"zinr": [(eq, "")],"flag": [(eq, 0)]})

            if mbill and mbill.saldo > 0:

                rguest = get_cache (Guest, {"gastnr": [(eq, mbill.gastnr)]})

                if rguest and rguest.zahlungsart == 0:
                    error_code = 3
                    co_ok = False
                    msg_str = translateExtended ("RoomNo", lvcarea, "") +\
                            " " + zinr + " - " +\
                            translateExtended ("Master Bill not yet settled.", lvcarea, "") + chr_unicode(10) +\
                            translateExtended ("Check-out not possible.", lvcarea, "") + chr_unicode(10)

                    return generate_output()
    co_ok = check_billstatus()

    if not co_ok:

        return generate_output()

    if case_type == 1:

        rline = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, res_line.zinr)],"l_zuordnung[2]": [(eq, 0)],"_recid": [(eq, res_line._recid)]})

        if rline:

            outorder = get_cache (Outorder, {"zinr": [(eq, res_line.zinr)],"gespstart": [(le, co_date)],"gespende": [(ge, co_date)],"betriebsnr": [(le, 1)]})

            if outorder:
                msg_int = 1
                msg_str = translateExtended ("Out-Of-Order Record found for this room:", lvcarea, "") + " " + to_string(outorder.gespstart) + "-" + to_string(outorder.gespende) + chr_unicode(10) + translateExtended ("The room status will immediately be changed to O-O-O after checking-out the guest.", lvcarea, "") + chr_unicode(10)
            early_co = (res_line.abreise > co_date)
            check_co_time()

            if early_co:

                if substring(bediener.permissions, 69, 1) >= ("2") :
                    msg_int = 2
                    msg_str = translateExtended ("Early Check-out", lvcarea, "") + " " + res_line.name + chr_unicode(10) + translateExtended ("ROOM", lvcarea, "") + " " + res_line.zinr + " ?" + chr_unicode(10)
                else:
                    msg_str = translateExtended ("No Access Right for Early Checkout [70,2].", lvcarea, "") + chr_unicode(10)
                    error_code = 4
            else:
                msg_int = 3
                msg_str = translateExtended ("Check-out", lvcarea, "") + " " + res_line.name + chr_unicode(10) + translateExtended ("ROOM", lvcarea, "") + " " + res_line.zinr + " ?" + chr_unicode(10)

        return generate_output()
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