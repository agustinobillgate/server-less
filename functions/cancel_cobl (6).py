#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.intevent_1 import intevent_1
from models import Res_line, Bediener, Zimkateg, Guest, Reservation, Reslin_queasy, Bill, Queasy, Zimmer, Master, Htparam, Zimplan, Resplan, Res_history

def cancel_cobl (6)(pvilanguage:int, inp_resnr:int, inp_reslinnr:int, co_date:date, user_init:string):

    prepare_cache ([Res_line, Bediener, Guest, Reservation, Reslin_queasy, Queasy, Zimmer, Master, Zimplan, Resplan, Res_history])

    msg_int = 0
    ankunft:date = None
    departure:date = None
    resnr:int = 49
    reslinnr:int = 1
    zinr:string = ""
    min_reslinnr:int = 0
    ci_date:date = None
    priscilla_active:bool = True
    res_line = bediener = zimkateg = guest = reservation = reslin_queasy = bill = queasy = zimmer = master = htparam = zimplan = resplan = res_history = None

    buf_rline = None

    Buf_rline = create_buffer("Buf_rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_int, ankunft, departure, resnr, reslinnr, zinr, min_reslinnr, ci_date, priscilla_active, res_line, bediener, zimkateg, guest, reservation, reslin_queasy, bill, queasy, zimmer, master, htparam, zimplan, resplan, res_history
        nonlocal pvilanguage, inp_resnr, inp_reslinnr, co_date, user_init
        nonlocal buf_rline


        nonlocal buf_rline

        return {"msg_int": msg_int}

    def guest_recheckin():

        nonlocal msg_int, ankunft, departure, resnr, reslinnr, zinr, min_reslinnr, ci_date, priscilla_active, res_line, bediener, zimkateg, guest, reservation, reslin_queasy, bill, queasy, zimmer, master, htparam, zimplan, resplan, res_history
        nonlocal pvilanguage, inp_resnr, inp_reslinnr, co_date, user_init
        nonlocal buf_rline


        nonlocal buf_rline

        bill1 = None
        bill2 = None
        res_line1 = None
        res_line2 = None
        resline = None
        zbuff = None
        qsy = None
        datum:date = None
        tot_umsatz:Decimal = to_decimal("0.0")
        i:int = 0
        upto_date:date = None
        iftask:string = ""
        origcode:string = ""
        cat_flag:bool = False
        roomnr:int = 0
        tmp_date:date = None
        Bill1 =  create_buffer("Bill1",Bill)
        Bill2 =  create_buffer("Bill2",Bill)
        Res_line1 =  create_buffer("Res_line1",Res_line)
        Res_line2 =  create_buffer("Res_line2",Res_line)
        Resline =  create_buffer("Resline",Res_line)
        Zbuff =  create_buffer("Zbuff",Zimkateg)
        Qsy =  create_buffer("Qsy",Queasy)

        zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})

        res_line1 = db_session.query(Res_line1).filter(
                 ((Res_line1.resnr != inp_resnr) & (Res_line1.reslinnr != inp_reslinnr)) & (Res_line1.zinr == (zinr).lower()) & ((Res_line1.resstatus == 6) | (Res_line1.resstatus == 13))).first()

        if not res_line1:
            pass
            zimmer.zistatus = 4
            zimmer.bediener_nr_stat = 0

            if res_line.abreise == ci_date:
                zimmer.zistatus = 3
            pass

        if res_line1:
            res_line.resstatus = 13
        else:
            res_line.resstatus = 6

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        if reservation.activeflag == 1:
            pass
            reservation.activeflag = 0
            pass

        if not res_line1:

            master = get_cache (Master, {"resnr": [(eq, resnr)]})

            if master:
                master.active = True
                pass
                msg_int = 1

                bill1 = db_session.query(Bill1).filter(
                         (Bill1.resnr == resnr) & (Bill1.reslinnr == 0)).first()

                if bill1:

                    if bill1.flag == 1:
                        pass
                        bill1.flag = 0
                        pass

                    if bill1.rechnr != 0:

                        guest = get_cache (Guest, {"gastnr": [(eq, bill1.gastnr)]})
                        guest.logisumsatz =  to_decimal(guest.logisumsatz) - to_decimal(bill1.logisumsatz)
                        guest.argtumsatz =  to_decimal(guest.argtumsatz) - to_decimal(bill1.argtumsatz)
                        guest.f_b_umsatz =  to_decimal(guest.f_b_umsatz) - to_decimal(bill1.f_b_umsatz)
                        guest.sonst_umsatz =  to_decimal(guest.sonst_umsatz) - to_decimal(bill1.sonst_umsatz)
                        guest.gesamtumsatz =  to_decimal(guest.gesamtumsatz) - to_decimal(bill1.gesamtumsatz)


                        pass
                        pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 307)]})

        if htparam.flogical:
            get_output(intevent_1(1, res_line.zinr, "RE-Checkin!", res_line.resnr, res_line.reslinnr))

        if priscilla_active:
            get_output(intevent_1(9, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))
        tmp_date = res_line.abreise - timedelta(days=1)

        if res_line.resstatus == 6:
            for datum in date_range(co_date,tmp_date) :

                zimplan = get_cache (Zimplan, {"zinr": [(eq, zinr)],"datum": [(eq, datum)]})

                if not zimplan:
                    zimplan = Zimplan()
                    db_session.add(zimplan)

                    zimplan.datum = datum
                    zimplan.zinr = zinr

        for resplan in db_session.query(Resplan).filter(
                 (Resplan.datum >= co_date) & (Resplan.datum < res_line.abreise) & (Resplan.zikatnr == zimmer.zikatnr)).order_by(Resplan._recid).all():
            resplan.anzzim[res_line.resstatus - 1] = resplan.anzzim[res_line.resstatus - 1] + 1
            pass

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.resnr = res_line.resnr
        res_history.reslinnr = res_line.reslinnr
        res_history.action = "RE-CI"


        res_history.aenderung = "Cancel C/O and Re-checkin by" + " " + user_init + " " + "ResNo" + " " + to_string(res_line.resnr) + " " + "RmNo" + " " + res_line.zinr

        res_line2 = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if res_line2:
            for i in range(1,num_entries(res_line2.zimmer_wunsch, ";") - 1 + 1) :
                iftask = entry(i - 1, res_line2.zimmer_wunsch, ";")

                if substring(iftask, 0, 10) == ("$origcode$").lower() :
                    origcode = substring(iftask, 10)
                    return

            queasy = get_cache (Queasy, {"key": [(eq, 152)]})

            if queasy:
                cat_flag = True

            zbuff = db_session.query(Zbuff).filter(
                     (Zbuff.zikatnr == res_line2.zikatnr)).first()

            if zbuff:

                if cat_flag:
                    roomnr = zbuff.typ
                else:
                    roomnr = zbuff.zikatnr

            if res_line2.ankunft == co_date:
                upto_date = co_date
            else:
                upto_date = res_line2.abreise - timedelta(days=1)
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
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.resnr = res_line2.resnr
            res_history.reslinnr = res_line2.reslinnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Cancel CO : ResNo " + to_string(res_line2.resnr) + " No " +\
                    to_string(res_line2.reslinnr) + " - " + res_line.name
            res_history.action = "Log Availability"

            if bediener:
                res_history.betriebsnr = bediener.nr
            pass

        for bill1 in db_session.query(Bill1).filter(
                 (Bill1.resnr == resnr) & (Bill1.parent_nr == reslinnr) & (Bill1.flag == 1) & (Bill1.zinr == (zinr).lower())).order_by(Bill1._recid).all():
            tot_umsatz =  to_decimal(tot_umsatz) + to_decimal(bill1.gesamtumsatz)

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

        for bill1 in db_session.query(Bill1).filter(
                 (Bill1.resnr == resnr) & (Bill1.parent_nr == reslinnr) & (Bill1.flag == 1) & (Bill1.zinr == (zinr).lower())).order_by(Bill1._recid).all():

            if tot_umsatz != 0:
                guest.logisumsatz =  to_decimal(guest.logisumsatz) - to_decimal(bill1.logisumsatz)
                guest.argtumsatz =  to_decimal(guest.argtumsatz) - to_decimal(bill1.argtumsatz)
                guest.f_b_umsatz =  to_decimal(guest.f_b_umsatz) - to_decimal(bill1.f_b_umsatz)
                guest.sonst_umsatz =  to_decimal(guest.sonst_umsatz) - to_decimal(bill1.sonst_umsatz)
                guest.gesamtumsatz =  to_decimal(guest.gesamtumsatz) - to_decimal(bill1.gesamtumsatz)


        pass

        bill2 = db_session.query(Bill2).filter(
                 (Bill2.resnr == res_line.resnr) & (Bill2.reslinnr == res_line.reslinnr)).first()
        bill2.flag = 0
        bill2.datum = co_date


        pass
        res_line.abreise = departure
        res_line.abreisezeit = 0
        res_line.changed = get_current_date()
        res_line.changed_id = user_init
        res_line.active_flag = 1

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest.zimmeranz > 0:
            guest.zimmeranz = guest.zimmeranz - 1

        if guest.aufenthalte > 0:
            guest.aufenthalte = guest.aufenthalte - 1
        guest.resflag = 2
        pass

        if res_line.gastnrmember != res_line.gastnrpay:
            get_min_reslinnr()

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

            if guest.zimmeranz > 0:
                guest.zimmeranz = guest.zimmeranz - 1

            if min_reslinnr == 1 and guest.aufenthalte > 0:
                guest.aufenthalte = guest.aufenthalte - 1


            pass

        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == res_line.resnr) & (Resline.kontakt_nr == res_line.reslinnr) & (Resline.l_zuordnung[inc_value(2)] == 1)).order_by(Resline._recid).all():
            resline.active_flag = 1
            resline.resstatus = 13
            resline.abreise = res_line.abreise
            resline.abreisezeit = 0
            resline.changed_id = user_init


    def get_min_reslinnr():

        nonlocal msg_int, ankunft, departure, resnr, reslinnr, zinr, min_reslinnr, ci_date, priscilla_active, res_line, bediener, zimkateg, guest, reservation, reslin_queasy, bill, queasy, zimmer, master, htparam, zimplan, resplan, res_history
        nonlocal pvilanguage, inp_resnr, inp_reslinnr, co_date, user_init
        nonlocal buf_rline


        nonlocal buf_rline

        resline = None
        Resline =  create_buffer("Resline",Res_line)

        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == resnr) & (Resline.active_flag == 1) & (Resline.resstatus != 12)).order_by(Resline._recid).all():
            min_reslinnr = min_reslinnr + 1

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    ci_date = get_output(htpdate(87))

    res_line = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, inp_reslinnr)]})

    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
    ankunft = res_line.ankunft
    departure = res_line.ankunft + timedelta(days=res_line.anztage)
    res_line.abreise = departure
    resnr = res_line.resnr
    reslinnr = res_line.reslinnr
    zinr = res_line.zinr
    guest_recheckin()
    pass

    buf_rline = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if buf_rline:
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = buf_rline.resnr
        reslin_queasy.reslinnr = buf_rline.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(buf_rline.name) + ";" + to_string("RE-CI CO GUEST") + ";" + to_string(" ") + ";" + to_string(" ") + ";"
        pass
        pass

    return generate_output()