from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpdate import htpdate
from functions.intevent_1 import intevent_1
from models import Res_line, Bediener, Zimkateg, Guest, Reservation, Reslin_queasy, Bill, Queasy, Zimmer, Master, Htparam, Zimplan, Resplan, Res_history

def cancel_cobl(pvilanguage:int, inp_resnr:int, inp_reslinnr:int, co_date:date, user_init:str):
    msg_int = 0
    ankunft:date = None
    departure:date = None
    resnr:int = 49
    reslinnr:int = 1
    zinr:str = ""
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
        tot_umsatz:decimal = to_decimal("0.0")
        i:int = 0
        upto_date:date = None
        iftask:str = ""
        origcode:str = ""
        cat_flag:bool = False
        roomnr:int = 0
        Bill1 =  create_buffer("Bill1",Bill)
        Bill2 =  create_buffer("Bill2",Bill)
        Res_line1 =  create_buffer("Res_line1",Res_line)
        Res_line2 =  create_buffer("Res_line2",Res_line)
        Resline =  create_buffer("Resline",Res_line)
        Zbuff =  create_buffer("Zbuff",Zimkateg)
        Qsy =  create_buffer("Qsy",Queasy)

        zimmer = db_session.query(Zimmer).filter(
                 (func.lower(Zimmer.zinr) == (zinr).lower())).first()

        res_line1 = db_session.query(Res_line1).filter(
                 ((Res_line1.resnr != inp_resnr) & (Res_line1.reslinnr != inp_reslinnr)) & (func.lower(Res_line1.zinr) == (zinr).lower()) & ((Res_line1.resstatus == 6) | (Res_line1.resstatus == 13))).first()

        if not res_line1:
            zimmer.zistatus = 4
            zimmer.bediener_nr_stat = 0

            if res_line.abreise == ci_date:
                zimmer.zistatus = 3

        if res_line1:
            res_line.resstatus = 13
        else:
            res_line.resstatus = 6

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == res_line.resnr)).first()

        if reservation.activeflag == 1:
            reservation.activeflag = 0

        if not res_line1:

            master = db_session.query(Master).filter(
                     (Master.resnr == resnr)).first()

            if master:
                master.active = True
                msg_int = 1

                bill1 = db_session.query(Bill1).filter(
                         (Bill1.resnr == resnr) & (Bill1.reslinnr == 0)).first()

                if bill1:

                    if bill1.flag == 1:
                        bill1.flag = 0

                    if bill1.rechnr != 0:

                        guest = db_session.query(Guest).filter(
                                 (Guest.gastnr == bill1.gastnr)).first()
                        guest.logisumsatz =  to_decimal(guest.logisumsatz) - to_decimal(bill1.logisumsatz)
                        guest.argtumsatz =  to_decimal(guest.argtumsatz) - to_decimal(bill1.argtumsatz)
                        guest.f_b_umsatz =  to_decimal(guest.f_b_umsatz) - to_decimal(bill1.f_b_umsatz)
                        guest.sonst_umsatz =  to_decimal(guest.sonst_umsatz) - to_decimal(bill1.sonst_umsatz)
                        guest.gesamtumsatz =  to_decimal(guest.gesamtumsatz) - to_decimal(bill1.gesamtumsatz)


                        pass

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 307)).first()

        if htparam.flogical:
            get_output(intevent_1(1, res_line.zinr, "RE-Checkin!", res_line.resnr, res_line.reslinnr))

        if priscilla_active:
            get_output(intevent_1(9, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        if res_line.resstatus == 6:
            for datum in date_range(co_date,(res_line.abreise - 1)) :

                zimplan = db_session.query(Zimplan).filter(
                         (func.lower(Zimplan.zinr) == (zinr).lower()) & (Zimplan.datum == datum)).first()

                if not zimplan:
                    zimplan = Zimplan()
                    db_session.add(zimplan)

                    zimplan.datum = datum
                    zimplan.zinr = zinr

        for resplan in db_session.query(Resplan).filter(
                 (Resplan.datum >= co_date) & (Resplan.datum < res_line.abreise) & (Resplan.zikatnr == zimmer.zikatnr)).order_by(Resplan._recid).all():
            resplan.anzzim[res_line.resstatus - 1] = resplan.anzzim[res_line.resstatus - 1] + 1
            pass

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == res_line.gastnrmember)).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.resnr = res_line.resnr
        res_history.reslinnr = res_line.reslinnr
        res_history.action = "RE-CI"


        res_history.aenderung = "Cancel C/O and Re-checkin by" + " " + user_init + " " + "ResNo" + " " + to_string(res_line.resnr) + " " + "RmNo" + " " + res_line.zinr

        res_line2 = db_session.query(Res_line2).filter(
                 (Res_line2.resnr == resnr) & (Res_line2.reslinnr == reslinnr)).first()

        if res_line2:
            for i in range(1,num_entries(res_line2.zimmer_wunsch, ";") - 1 + 1) :
                iftask = entry(i - 1, res_line2.zimmer_wunsch, ";")

                if substring(iftask, 0, 10) == ("$origcode$").lower() :
                    origcode = substring(iftask, 10)
                    return

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 152)).first()

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

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 171) & (Queasy.date1 == datum) & (Queasy.number1 == roomnr) & (Queasy.char1 == "")).first()

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    qsy = db_session.query(Qsy).filter(
                             (Qsy._recid == queasy._recid)).first()

                    if qsy:
                        qsy.logi2 = True
                        pass

                if origcode != "":

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 171) & (Queasy.date1 == datum) & (Queasy.number1 == roomnr) & (func.lower(Queasy.char1) == (origcode).lower())).first()

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:

                        qsy = db_session.query(Qsy).filter(
                                 (Qsy._recid == queasy._recid)).first()

                        if qsy:
                            qsy.logi2 = True
                            pass

        for bill1 in db_session.query(Bill1).filter(
                 (Bill1.resnr == resnr) & (Bill1.parent_nr == reslinnr) & (Bill1.flag == 1) & (func.lower(Bill1.zinr) == (zinr).lower())).order_by(Bill1._recid).all():
            tot_umsatz =  to_decimal(tot_umsatz) + to_decimal(bill1.gesamtumsatz)

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == res_line.gastnrpay)).first()

        for bill1 in db_session.query(Bill1).filter(
                 (Bill1.resnr == resnr) & (Bill1.parent_nr == reslinnr) & (Bill1.flag == 1) & (func.lower(Bill1.zinr) == (zinr).lower())).order_by(Bill1._recid).all():

            if tot_umsatz != 0:
                guest.logisumsatz =  to_decimal(guest.logisumsatz) - to_decimal(bill1.logisumsatz)
                guest.argtumsatz =  to_decimal(guest.argtumsatz) - to_decimal(bill1.argtumsatz)
                guest.f_b_umsatz =  to_decimal(guest.f_b_umsatz) - to_decimal(bill1.f_b_umsatz)
                guest.sonst_umsatz =  to_decimal(guest.sonst_umsatz) - to_decimal(bill1.sonst_umsatz)
                guest.gesamtumsatz =  to_decimal(guest.gesamtumsatz) - to_decimal(bill1.gesamtumsatz)

        bill2 = db_session.query(Bill2).filter(
                 (Bill2.resnr == res_line.resnr) & (Bill2.reslinnr == res_line.reslinnr)).first()
        bill2.flag = 0
        bill2.datum = co_date


        res_line.abreise = departure
        res_line.abreisezeit = 0
        res_line.changed = get_current_date()
        res_line.changed_id = user_init
        res_line.active_flag = 1

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == res_line.gastnrmember)).first()

        if guest.zimmeranz > 0:
            guest.zimmeranz = guest.zimmeranz - 1

        if guest.aufenthalte > 0:
            guest.aufenthalte = guest.aufenthalte - 1
        guest.resflag = 2

        if res_line.gastnrmember != res_line.gastnrpay:
            get_min_reslinnr()

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrpay)).first()

            if guest.zimmeranz > 0:
                guest.zimmeranz = guest.zimmeranz - 1

            if min_reslinnr == 1 and guest.aufenthalte > 0:
                guest.aufenthalte = guest.aufenthalte - 1

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

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()
    ci_date = get_output(htpdate(87))

    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == inp_resnr) & (Res_line.reslinnr == inp_reslinnr)).first()

    zimkateg = db_session.query(Zimkateg).filter(
             (Zimkateg.zikatnr == res_line.zikatnr)).first()

    guest = db_session.query(Guest).filter(
             (Guest.gastnr == res_line.gastnrmember)).first()

    reservation = db_session.query(Reservation).filter(
             (Reservation.resnr == res_line.resnr)).first()
    ankunft = res_line.ankunft
    departure = res_line.ankunft + timedelta(days=res_line.anztage)
    res_line.abreise = departure
    resnr = res_line.resnr
    reslinnr = res_line.reslinnr
    zinr = res_line.zinr
    guest_recheckin()

    buf_rline = db_session.query(Buf_rline).filter(
             (Buf_rline.resnr == resnr) & (Buf_rline.reslinnr == reslinnr)).first()

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

    return generate_output()