from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpdate import htpdate
from functions.intevent_1 import intevent_1
from models import Res_line, Bediener, Zimkateg, Guest, Reservation, Reslin_queasy, Bill, Zimmer, Master, Htparam, Zimplan, Resplan, Res_history

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
    res_line = bediener = zimkateg = guest = reservation = reslin_queasy = bill = zimmer = master = htparam = zimplan = resplan = res_history = None

    buf_rline = bill1 = bill2 = res_line1 = res_line2 = resline = None

    Buf_rline = Res_line
    Bill1 = Bill
    Bill2 = Bill
    Res_line1 = Res_line
    Res_line2 = Res_line
    Resline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_int, ankunft, departure, resnr, reslinnr, zinr, min_reslinnr, ci_date, priscilla_active, res_line, bediener, zimkateg, guest, reservation, reslin_queasy, bill, zimmer, master, htparam, zimplan, resplan, res_history
        nonlocal buf_rline, bill1, bill2, res_line1, res_line2, resline


        nonlocal buf_rline, bill1, bill2, res_line1, res_line2, resline
        return {"msg_int": msg_int}

    def guest_recheckin():

        nonlocal msg_int, ankunft, departure, resnr, reslinnr, zinr, min_reslinnr, ci_date, priscilla_active, res_line, bediener, zimkateg, guest, reservation, reslin_queasy, bill, zimmer, master, htparam, zimplan, resplan, res_history
        nonlocal buf_rline, bill1, bill2, res_line1, res_line2, resline


        nonlocal buf_rline, bill1, bill2, res_line1, res_line2, resline

        datum:date = None
        tot_umsatz:decimal = 0
        Bill1 = Bill
        Bill2 = Bill
        Res_line1 = Res_line
        Res_line2 = Res_line
        Resline = Res_line

        zimmer = db_session.query(Zimmer).filter(
                (func.lower(Zimmer.(zinr).lower()) == (zinr).lower())).first()

        res_line1 = db_session.query(Res_line1).filter(
                ((Res_line1.resnr != inp_resnr) &  (Res_line1.reslinnr != inp_reslinnr)) &  (func.lower(Res_line1.(zinr).lower()) == (zinr).lower()) &  ((Res_line1.resstatus == 6) |  (Res_line1.resstatus == 13))).first()

        if not res_line1:

            zimmer = db_session.query(Zimmer).first()
            zimmer.zistatus = 4
            zimmer.bediener_nr_stat = 0

            if res_line.abreise == ci_date:
                zimmer.zistatus = 3

            zimmer = db_session.query(Zimmer).first()

        if res_line1:
            res_line.resstatus = 13
        else:
            res_line.resstatus = 6

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == res_line.resnr)).first()

        if reservation.activeflag == 1:

            reservation = db_session.query(Reservation).first()
            reservation.activeflag = 0

            reservation = db_session.query(Reservation).first()

        if not res_line1:

            master = db_session.query(Master).filter(
                    (Master.resnr == resnr)).first()

            if master:
                master.active = True

                master = db_session.query(Master).first()
                msg_int = 1

                bill1 = db_session.query(Bill1).filter(
                        (Bill1.resnr == resnr) &  (Bill1.reslinnr == 0)).first()

                if bill1:

                    if bill1.flag == 1:

                        bill1 = db_session.query(Bill1).first()
                        bill1.flag = 0

                        bill1 = db_session.query(Bill1).first()

                    if bill1.rechnr != 0:

                        guest = db_session.query(Guest).filter(
                                (Guest.gastnr == bill1.gastnr)).first()
                        guest.logisumsatz = guest.logisumsatz - bill1.logisumsatz
                        guest.argtumsatz = guest.argtumsatz - bill1.argtumsatz
                        guest.f_b_umsatz = guest.f_b_umsatz - bill1.f_b_umsatz
                        guest.sonst_umsatz = guest.sonst_umsatz - bill1.sonst_umsatz
                        guest.gesamtumsatz = guest.gesamtumsatz - bill1.gesamtumsatz

                        guest = db_session.query(Guest).first()


        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 307)).first()

        if htparam.flogical:
            get_output(intevent_1(1, res_line.zinr, "RE_Checkin!", res_line.resnr, res_line.reslinnr))

        if priscilla_active:
            get_output(intevent_1(9, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        if res_line.resstatus == 6:
            for datum in range(co_date,(res_line.abreise - 1)  + 1) :

                zimplan = db_session.query(Zimplan).filter(
                        (func.lower(Zimplan.(zinr).lower()) == (zinr).lower()) &  (Zimplan.datum == datum)).first()

                if not zimplan:
                    zimplan = Zimplan()
                    db_session.add(zimplan)

                    zimplan.datum = datum
                    zimplan.zinr = zinr

        for resplan in db_session.query(Resplan).filter(
                (Resplan.datum >= co_date) &  (Resplan.datum < res_line.abreise) &  (Resplan.zikatnr == zimmer.zikatnr)).all():
            resplan.anzzim[res_line.resstatus - 1] = resplan.anzzim[res_line.resstatus - 1] + 1


        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.resnr = res_line.resnr
        res_history.reslinnr = res_line.reslinnr
        res_history.action = "RE_CI"


        res_history.aenderung = "Cancel C/O and Re_checkin by" + " " + user_init + " " + "ResNo" + " " + to_string(res_line.resnr) + " " + "RmNo" + " " + res_line.zinr

        for bill1 in db_session.query(Bill1).filter(
                (Bill1.resnr == resnr) &  (Bill1.parent_nr == reslinnr) &  (Bill1.flag == 1) &  (func.lower(Bill1.(zinr).lower()) == (zinr).lower())).all():
            tot_umsatz = tot_umsatz + bill1.gesamtumsatz

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrpay)).first()

        for bill1 in db_session.query(Bill1).filter(
                (Bill1.resnr == resnr) &  (Bill1.parent_nr == reslinnr) &  (Bill1.flag == 1) &  (func.lower(Bill1.(zinr).lower()) == (zinr).lower())).all():

            if tot_umsatz != 0:
                guest.logisumsatz = guest.logisumsatz - bill1.logisumsatz
                guest.argtumsatz = guest.argtumsatz - bill1.argtumsatz
                guest.f_b_umsatz = guest.f_b_umsatz - bill1.f_b_umsatz
                guest.sonst_umsatz = guest.sonst_umsatz - bill1.sonst_umsatz
                guest.gesamtumsatz = guest.gesamtumsatz - bill1.gesamtumsatz

        guest = db_session.query(Guest).first()

        bill2 = db_session.query(Bill2).filter(
                (Bill2.resnr == res_line.resnr) &  (Bill2.reslinnr == res_line.reslinnr)).first()
        bill2.flag = 0
        bill2.datum = co_date

        bill2 = db_session.query(Bill2).first()
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

        guest = db_session.query(Guest).first()

        if res_line.gastnrmember != res_line.gastnrpay:
            get_min_reslinnr()

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrpay)).first()

            if guest.zimmeranz > 0:
                guest.zimmeranz = guest.zimmeranz - 1

            if min_reslinnr == 1 and guest.aufenthalte > 0:
                guest.aufenthalte = guest.aufenthalte - 1

            guest = db_session.query(Guest).first()

        for resline in db_session.query(Resline).filter(
                (Resline.resnr == res_line.resnr) &  (Resline.kontakt_nr == res_line.reslinnr) &  (Resline.l_zuordnung[2] == 1)).all():
            resline.active_flag = 1
            resline.resstatus = 13
            resline.abreise = res_line.abreise
            resline.abreisezeit = 0
            resline.changed_id = user_init

    def get_min_reslinnr():

        nonlocal msg_int, ankunft, departure, resnr, reslinnr, zinr, min_reslinnr, ci_date, priscilla_active, res_line, bediener, zimkateg, guest, reservation, reslin_queasy, bill, zimmer, master, htparam, zimplan, resplan, res_history
        nonlocal buf_rline, bill1, bill2, res_line1, res_line2, resline


        nonlocal buf_rline, bill1, bill2, res_line1, res_line2, resline


        Resline = Res_line

        for resline in db_session.query(Resline).filter(
                (Resline.resnr == resnr) &  (Resline.active_flag == 1) &  (Resline.resstatus != 12)).all():
            min_reslinnr = min_reslinnr + 1


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    ci_date = get_output(htpdate(87))

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == inp_resnr) &  (Res_line.reslinnr == inp_reslinnr)).first()

    zimkateg = db_session.query(Zimkateg).filter(
            (Zimkateg.zikatnr == res_line.zikatnr)).first()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == res_line.gastnrmember)).first()

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == res_line.resnr)).first()
    ankunft = res_line.ankunft
    departure = res_line.ankunft + res_line.anztage
    res_line.abreise = departure
    resnr = res_line.resnr
    reslinnr = res_line.reslinnr
    zinr = res_line.zinr
    guest_recheckin()

    res_line = db_session.query(Res_line).first()

    buf_rline = db_session.query(Buf_rline).filter(
            (Buf_rline.resnr == resnr) &  (Buf_rline.reslinnr == reslinnr)).first()

    if buf_rline:
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = buf_rline.resnr
        reslin_queasy.reslinnr = buf_rline.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(buf_rline.name) + ";" + to_string("RE_CI CO GUEST") + ";" + to_string(" ") + ";" + to_string(" ") + ";"

        reslin_queasy = db_session.query(Reslin_queasy).first()


    return generate_output()