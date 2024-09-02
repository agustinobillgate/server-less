from functions.additional_functions import *
import decimal
from datetime import date
from functions.check_timebl import check_timebl
from sqlalchemy import func
from models import Reservation, Bediener, Master, Res_line, Guest, Htparam, Bill, Counters, Res_history, Guest_pr, Segment, Reslin_queasy

def mk_mainres_btn_gobl(pvilanguage:int, inp_resnr:int, resart:int, last_segm:int, curr_segm:int, gastnrherk:int, gastnrcom:int, gastnrpay:int, letterno:int, contact_nr:int, rechnerstart:int, rechnrend:int, res_mode:str, user_init:str, origin:str, groupname:str, comments:str, voucherno:str, bill_receiver:str, depositgef:decimal, limitdate:date, fixed_rate:bool, init_rate:bool, master_active:bool, umsatz1:bool, umsatz2:bool, umsatz3:bool, umsatz4:bool, init_time:int, init_date:date):
    flag_ok = False
    msg_str = ""
    error_number = 0
    segmstr:str = ""
    a:int = 0
    b:date = None
    lvcarea:str = "mk_mainres"
    reservation = bediener = master = res_line = guest = htparam = bill = counters = res_history = guest_pr = segment = reslin_queasy = None

    segment1 = None

    Segment1 = Segment

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag_ok, msg_str, error_number, segmstr, a, b, lvcarea, reservation, bediener, master, res_line, guest, htparam, bill, counters, res_history, guest_pr, segment, reslin_queasy
        nonlocal segment1


        nonlocal segment1
        return {"flag_ok": flag_ok, "msg_str": msg_str, "error_number": error_number}

    def mk_mainres_go():

        nonlocal flag_ok, msg_str, error_number, segmstr, a, b, lvcarea, reservation, bediener, master, res_line, guest, htparam, bill, counters, res_history, guest_pr, segment, reslin_queasy
        nonlocal segment1


        nonlocal segment1

        last_segm:int = 0
        prev_gastnr:int = 0
        incorrect:bool = False
        chg_member:bool = False
        num_chg:int = 0
        contrate_found:bool = False
        curr_name:str = ""
        check_segm()

        if error_number > 0:

            return

        if resart == 0:
            msg_str = translateExtended ("Source of Booking not defined.", lvcarea, "")
            error_number = 2

            return

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == inp_resnr)).first()

        if not reservation:
            msg_str = translateExtended ("Reservation record is being used by other user.", lvcarea, "")
            error_number = 3

            return

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()
        prev_gastnr = reservation.gastnr

        master = db_session.query(Master).filter(
                (Master.resnr == reservation.resnr)).first()

        if master and master.active:
            reservation.verstat = 1
        else:
            reservation.verstat = 0

        if res_mode.lower()  == "new":
            reservation.useridanlage = user_init

        elif res_mode.lower()  == "modify":
            reservation.useridmutat = user_init
            reservation.mutdat = get_current_date()

        if res_mode.lower()  != "new" and ((reservation.segmentcode != curr_segm) or (reservation.bemerk != comments)):
            add_reslog(reservation.segmentcode, curr_segm)
        reservation.segmentcode = curr_segm
        reservation.groupname = groupname
        reservation.grpflag = (groupname != "")
        reservation.bemerk = comments
        reservation.limitdate = limitdate
        reservation.depositgef = depositgef
        reservation.gastnrherk = gastnrherk
        reservation.herkunft = origin
        reservation.guestnrcom[0] = gastnrcom
        reservation.briefnr = letterno
        reservation.resart = resart
        reservation.vesrdepot = voucherno
        reservation.insurance = fixed_rate
        reservation.kontakt_nr = contact_nr

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == reservation.resnr) &  (Res_line.active_flag <= 1)).first()
        while None != res_line:

            res_line = db_session.query(Res_line).first()

            if res_line:
                res_line.grpflag = reservation.grpflag

                res_line = db_session.query(Res_line).first()

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == reservation.resnr)).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == reservation.gastnr)).first()

        if not master and (guest.karteityp == 1 or guest.karteityp == 2):

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 166)).first()

            if htparam.flogical:
                msg_str = "&Q" + translateExtended ("Master Bill does not exist, CREATE IT?", lvcarea, "")

        if master:

            master = db_session.query(Master).first()
            master.ACTIVE = master_active
            master.rechnrstart = rechnrstart
            master.rechnrend = rechnrend
            master.umsatzart[0] = umsatz1
            master.umsatzart[1] = umsatz2
            master.umsatzart[2] = umsatz3
            master.umsatzart[3] = umsatz4
            master.gastnrpay = gastnrpay
            master.name = bill_receiver

            if not master.active:

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == inp_resnr) &  (Bill.reslinnr == 0)).first()

                if bill and bill.saldo != 0:
                    master.active = True

            master = db_session.query(Master).first()

            if master.active:
                reservation.verstat = 1
            else:
                reservation.verstat = 0

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == master.resnr) &  (Res_line.active_flag == 1)).first()

            if res_line:

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == inp_resnr) &  (Bill.reslinnr == 0)).first()

                if not bill:
                    bill = Bill()
                    db_session.add(bill)

                    bill.resnr = inp_resnr
                    bill.reslinnr = 0
                    bill.rgdruck = 1
                    billtyp = 2

                    if master.rechnr != 0:
                        bill.rechnr = master.rechnr
                    else:

                        counters = db_session.query(Counters).filter(
                                (Counters.counter_no == 3)).first()
                        counters = counters + 1
                        bill.rechnr = counters

                        counters = db_session.query(Counters).first()

                        master = db_session.query(Master).first()
                        master.rechnr = bill.rechnr

                        master = db_session.query(Master).first()
                bill.gastnr = gastnrpay
                bill.name = bill_receiver
                bill.segmentcode = curr_segm

                bill = db_session.query(Bill).first()

        if (reservation.insurance and not init_rate) or (not reservation.insurance and init_rate):
            resline_reserve_dec()

        if reservation.gastnr != gastnrherk:
            curr_name = reservation.name

            reservation = db_session.query(Reservation).first()
            reservation.gastnr = gastnrherk

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == gastnrherk)).first()
            reservation.name = guest.name + ", " + guest.vorname1 + guest.anredefirma

            reservation = db_session.query(Reservation).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Reservation"
            res_history.aenderung = "CHG Reservation Name " + curr_name +\
                    " -> " + reservation.name

            res_history = db_session.query(Res_history).first()

            master = db_session.query(Master).filter(
                    (Master.resnr == reservation.resnr)).first()

            if master:
                master.gastnr = gastnrherk
                master.gastnrpay = gastnrherk
                master.name = reservation.name

                master = db_session.query(Master).first()

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == reservation.resnr) &  (Bill.reslinnr == 0)).first()

                if bill:
                    bill.gastnr = gastnrherk
                    bill.name = guest.name

                    bill = db_session.query(Bill).first()

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.resnr == reservation.resnr) &  (Res_line.reslinnr >= 1)).all():
                res_line.gastnr = gastnrherk

                if res_line.gastnrpay == prev_gastnr:

                    for bill in db_session.query(Bill).filter(
                            (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr) &  (Bill.zinr == res_line.zinr)).all():
                        bill.gastnr = gastnrherk
                        bill.name = guest.name
                    res_line.gastnrpay = gastnrherk

                if res_line.gastnrmember == prev_gastnr and res_line.active_flag == 0:
                    num_chg = num_chg + 1
                res_line.resname = reservation.name

            guest_pr = db_session.query(Guest_pr).filter(
                    (Guest_pr.gastnr == reservation.gastnr)).first()

            if not guest_pr:

                guest_pr = db_session.query(Guest_pr).filter(
                        (Guest_pr.gastnr == gastnrherk)).first()

            if guest_pr:
                msg_str = "&W" + translateExtended ("Contract Rate exists", lvcarea, "") + chr(10) + translateExtended ("Manual Changes of the room rate(s) required.", lvcarea, "")

    def check_segm():

        nonlocal flag_ok, msg_str, error_number, segmstr, a, b, lvcarea, reservation, bediener, master, res_line, guest, htparam, bill, counters, res_history, guest_pr, segment, reslin_queasy
        nonlocal segment1


        nonlocal segment1

        i:int = 0
        b_list:int = 0

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == curr_segm)).first()

        if not segment:
            msg_str = translateExtended ("No such segmentcode.", lvcarea, "")
            error_number = 1

            return

        if segment.betriebsnr == 3:
            error_number = 1

            return

        if segment.betriebsnr == 4:
            error_number = 1

            return

        if segment.betriebsnr >= 1 and segment.betriebsnr <= 2:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == inp_resnr) &  (Res_line.active_flag <= 1) &  (Res_line.zipreis > 0)).first()

            if res_line:
                msg_str = translateExtended ("The selected COMPLIMENT segment is not valid:", lvcarea, "") + chr(10) + translateExtended ("Reservation record found with non_zero RmRate  == ", lvcarea, "") + " " + to_string(res_line.zipreis)
                error_number = 1

                return
        segmstr = entry(0, segment.bezeich, "$$0")

    def add_reslog(old_segm:int, new_segm:int):

        nonlocal flag_ok, msg_str, error_number, segmstr, a, b, lvcarea, reservation, bediener, master, res_line, guest, htparam, bill, counters, res_history, guest_pr, segment, reslin_queasy
        nonlocal segment1


        nonlocal segment1

        cdate:date = get_current_date()
        heute:date = None
        zeit:int = 0
        Segment1 = Segment

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == inp_resnr) &  (Res_line.active_flag == 1) &  (Res_line.resstatus == 6)).first()

        if not res_line:

            if (reservation.bemerk == comments):

                return

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == inp_resnr) &  (Res_line.active_flag == 0) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5))).first()

            if not res_line:

                return
        heute = get_current_date()
        zeit = get_current_time_in_seconds()

        if reservation.mutdat != None:
            cdate = reservation.mutdat

        segment1 = db_session.query(Segment1).filter(
                (Segment1.segmentcode == reservation.segmentcode)).first()

        if segment1:
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "ResChanges"
            reslin_queasy.resnr = res_line.resnr
            reslin_queasy.reslinnr = res_line.reslinnr
            reslin_queasy.date2 = heute
            reslin_queasy.number2 = zeit

            if reservation.segmentcode != curr_segm:
                reslin_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string("SEGM") + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(reservation.useridanlage) + ";" + to_string(user_init) + ";" + to_string(cdate) + ";" + to_string(heute) + ";" + to_string(segment1.bezeich) + ";" + to_string(segmstr) + ";" + to_string(" ") + ";" + to_string(" ") + ";"
            else:
                reslin_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(reservation.useridanlage) + ";" + to_string(user_init) + ";" + to_string(cdate) + ";" + to_string(heute) + ";" + to_string(segment1.bezeich) + ";" + to_string(segment1.bezeich) + ";" + to_string(" ") + ";" + to_string(" ") + ";"

            reslin_queasy = db_session.query(Reslin_queasy).first()


        if reservation.bemerk.lower()  != (comments).lower() :
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.resnr = res_line.resnr
            res_history.reslinnr = res_line.reslinnr
            res_history.datum = heute
            res_history.zeit = zeit
            res_history.action = "MainRes Remark"
            res_history.aenderung = reservation.bemerk +\
                    "*** Changed to: " + comments

            res_history = db_session.query(Res_history).first()


    flag_ok, a, b = get_output(check_timebl(3, inp_resnr, None, "reservation", init_time, init_date))

    if not flag_ok:

        return generate_output()
    mk_mainres_go()

    return generate_output()