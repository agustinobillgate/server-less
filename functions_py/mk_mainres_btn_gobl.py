#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 17/10/2025
# lower di boolean, err
#------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#----------------------------------------

# ====================================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# - Fix variable name from rechnrstart to rechnerstart
# - Fix procedure in progress not used
# ====================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.check_timebl import check_timebl
from models import Bill, Reservation, Bediener, Master, Res_line, Guest, Htparam, Counters, Res_history, Guest_pr, Segment, Reslin_queasy
from functions.next_counter_for_update import next_counter_for_update

def mk_mainres_btn_gobl(pvilanguage:int, inp_resnr:int, resart:int, last_segm:int, curr_segm:int, gastnrherk:int, 
                        gastnrcom:int, gastnrpay:int, letterno:int, contact_nr:int, rechnerstart:int, rechnrend:int, 
                        res_mode:string, user_init:string, origin:string, groupname:string, comments:string, 
                        voucherno:string, bill_receiver:string, depositgef:Decimal, limitdate:date, fixed_rate:bool, 
                        init_rate:bool, master_active:bool, umsatz1:bool, umsatz2:bool, umsatz3:bool, umsatz4:bool, 
                        init_time:int, init_date:date):

    prepare_cache ([Reservation, Bediener, Master, Guest, Counters, Res_history, Segment, Reslin_queasy])

    flag_ok = False
    msg_str = ""
    error_number = 0
    segmstr:string = ""
    a:int = 0
    b:date = None
    lvcarea:string = "mk-mainres"
    bill = reservation = bediener = master = res_line = guest = htparam = counters = res_history = guest_pr = segment = reslin_queasy = None

    buff_bill = None

    Buff_bill = create_buffer("Buff_bill",Bill)


    db_session = local_storage.db_session
    res_mode = res_mode.strip()
    user_init = user_init.strip()
    origin = origin.strip()
    groupname = groupname.strip()
    comments = comments.strip()
    voucherno = voucherno.strip()
    bill_receiver = bill_receiver.strip()
    last_count = 0
    error_lock:string = ""

    def generate_output():
        nonlocal flag_ok, msg_str, error_number, segmstr, a, b, lvcarea, bill, reservation, bediener, master, res_line, guest, htparam, counters, res_history, guest_pr, segment, reslin_queasy
        nonlocal pvilanguage, inp_resnr, resart, last_segm, curr_segm, gastnrherk, gastnrcom, gastnrpay, letterno, contact_nr, rechnerstart, rechnrend, res_mode, user_init, origin, groupname, comments, voucherno, bill_receiver, depositgef, limitdate, fixed_rate, init_rate, master_active, umsatz1, umsatz2, umsatz3, umsatz4, init_time, init_date
        nonlocal buff_bill


        nonlocal buff_bill

        return {"flag_ok": flag_ok, "msg_str": msg_str, "error_number": error_number}

    def mk_mainres_go():

        nonlocal flag_ok, msg_str, error_number, segmstr, a, b, lvcarea, bill, reservation, bediener, master, res_line, guest, htparam, counters, res_history, guest_pr, segment, reslin_queasy
        nonlocal pvilanguage, inp_resnr, resart, curr_segm, gastnrherk, gastnrcom, gastnrpay, letterno, contact_nr, rechnerstart, rechnrend, res_mode, user_init, origin, groupname, comments, voucherno, bill_receiver, depositgef, limitdate, fixed_rate, init_rate, master_active, umsatz1, umsatz2, umsatz3, umsatz4, init_time, init_date
        nonlocal buff_bill


        nonlocal buff_bill

        last_segm:int = 0
        prev_gastnr:int = 0
        incorrect:bool = False
        chg_member:bool = False
        num_chg:int = 0
        contrate_found:bool = False
        curr_name:string = ""
        check_segm()

        if error_number > 0:

            return

        if resart == 0:
            msg_str = translateExtended ("Source of Booking not defined.", lvcarea, "")
            error_number = 2

            return

        # reservation = get_cache (Reservation, {"resnr": [(eq, inp_resnr)]})
        reservation = db_session.query(Reservation).filter(Reservation.resnr == inp_resnr).with_for_update().with_for_update().first()

        if not reservation:
            msg_str = translateExtended ("Reservation record is being used by other user.", lvcarea, "")
            error_number = 3

            return

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        prev_gastnr = reservation.gastnr

        # master = get_cache (Master, {"resnr": [(eq, reservation.resnr)]})
        master = db_session.query(Master).filter(Master.resnr == reservation.resnr).with_for_update().first()

        if master and master.active:
            reservation.verstat = 1
        else:
            reservation.verstat = 0

        if res_mode  == ("new") :
            reservation.useridanlage = user_init

        elif res_mode  == ("modify") :
            reservation.useridmutat = user_init
            reservation.mutdat = get_current_date()

        if res_mode  != ("new")  and ((reservation.segmentcode != curr_segm) or (reservation.bemerk  != (comments))):
            add_reslog(reservation.segmentcode, curr_segm)
        reservation.segmentcode = curr_segm
        reservation.groupname = groupname
        reservation.grpflag = (groupname != "")
        reservation.bemerk = comments
        reservation.limitdate = limitdate
        reservation.depositgef =  to_decimal(depositgef)
        reservation.gastnrherk = gastnrherk
        reservation.herkunft = origin
        reservation.guestnrcom[0] = gastnrcom
        reservation.briefnr = letterno
        reservation.resart = resart
        reservation.vesrdepot = voucherno
        reservation.insurance = fixed_rate
        reservation.kontakt_nr = contact_nr

        # res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"active_flag": [(le, 1)]})
        res_line = db_session.query(Res_line).filter(Res_line.resnr == reservation.resnr, Res_line.active_flag <= 1).with_for_update().first()

        while None != res_line:
            pass

            if res_line:
                res_line.grpflag = reservation.grpflag
                db_session.refresh(res_line, with_for_update=True)

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == reservation.resnr) & (Res_line._recid > curr_recid)).first()

        guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

        if not master and (guest.karteityp == 1 or guest.karteityp == 2):

            htparam = get_cache (Htparam, {"paramnr": [(eq, 166)]})

            if htparam.flogical:
                msg_str = "&Q" + translateExtended ("Master Bill does not exist, CREATE IT?", lvcarea, "")

        if master:

            if master_active != master.active:
                pass
            pass
            master.active = master_active
            master.rechnrstart = rechnerstart                   # Rulita, 27-11-2025 | Fix variable name from rechnrstart to rechnerstart
            master.rechnrend = rechnrend
            master.umsatzart[0] = umsatz1
            master.umsatzart[1] = umsatz2
            master.umsatzart[2] = umsatz3
            master.umsatzart[3] = umsatz4
            master.gastnrpay = gastnrpay
            master.name = bill_receiver

            if not master.active:

                bill = get_cache (Bill, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, 0)]})

                if bill and bill.saldo != 0:
                    master.active = True
            
            db_session.refresh(master, with_for_update=True)

            if master.active:
                reservation.verstat = 1
            else:
                reservation.verstat = 0

            res_line = get_cache (Res_line, {"resnr": [(eq, master.resnr)],"active_flag": [(eq, 1)]})

            if res_line:

                # bill = get_cache (Bill, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, 0)]})
                bill = db_session.query(Bill).filter(Bill.resnr == inp_resnr, Bill.reslinnr == 0).with_for_update().first()

                if not bill:
                    bill = Bill()
                    db_session.add(bill)

                    bill.resnr = inp_resnr
                    bill.reslinnr = 0
                    bill.rgdruck = 1
                    bill.billtyp = 2

                    if master.rechnr != 0:
                        bill.rechnr = master.rechnr
                    else:

                        # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                        # counters.counter = counters.counter + 1
                        # bill.rechnr = counters.counter
                        # pass
                        # pass
                        # master.rechnr = bill.rechnr
                        last_count, error_lock = get_output(next_counter_for_update(3))
                        bill.rechnr = last_count
                        
                        pass
                bill.gastnr = gastnrpay
                bill.name = bill_receiver
                bill.segmentcode = curr_segm


                pass

                buff_bill = db_session.query(Buff_bill).filter(
                         (Buff_bill.rechnr == bill.rechnr) & (Buff_bill.resnr == 0) & (Buff_bill.reslinnr == 1) & (Buff_bill.billtyp != 2)).first()

                if buff_bill:
                    pass
                    db_session.delete(buff_bill)
                    pass
        
        # Rulita, 27-11-2025 | Fix in progress not used
        # if (reservation.insurance and not init_rate) or (not reservation.insurance and init_rate):
        #     resline_reserve_dec()

        if reservation.gastnr != gastnrherk:
            curr_name = reservation.name
            pass
            reservation.gastnr = gastnrherk

            guest = get_cache (Guest, {"gastnr": [(eq, gastnrherk)]})
            reservation.name = guest.name + ", " + guest.vorname1 + guest.anredefirma
            pass
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Reservation"
            res_history.aenderung = "CHG Reservation Name " + curr_name +\
                    " -> " + reservation.name


            pass

            # master = get_cache (Master, {"resnr": [(eq, reservation.resnr)]})
            master = db_session.query(Master).filter(Master.resnr == reservation.resnr).with_for_update().first()

            if master:
                master.gastnr = gastnrherk
                master.gastnrpay = gastnrherk
                master.name = reservation.name
                pass

                # bill = get_cache (Bill, {"resnr": [(eq, reservation.resnr)],"reslinnr": [(eq, 0)]})
                bill = db_session.query(Bill).filter(Bill.resnr == reservation.resnr, Bill.reslinnr == 0).with_for_update().first()

                if bill:
                    bill.gastnr = gastnrherk
                    bill.name = guest.name
                    pass

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == reservation.resnr) & (Res_line.reslinnr >= 1)).order_by(Res_line._recid).with_for_update().all():
                res_line.gastnr = gastnrherk

                if res_line.gastnrpay == prev_gastnr:

                    for bill in db_session.query(Bill).filter(
                             (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr) & (Bill.zinr == res_line.zinr)).order_by(Bill._recid).with_for_update().all():
                        bill.gastnr = gastnrherk
                        bill.name = guest.name
                    res_line.gastnrpay = gastnrherk

                if res_line.gastnrmember == prev_gastnr and res_line.active_flag == 0:
                    num_chg = num_chg + 1
                res_line.resname = reservation.name

            guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, reservation.gastnr)]})

            if not guest_pr:

                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, gastnrherk)]})

            if guest_pr:
                msg_str = "&W" + translateExtended ("Contract Rate exists", lvcarea, "") + chr_unicode(10) + translateExtended ("Manual Changes of the room rate(s) required.", lvcarea, "")


    def check_segm():

        nonlocal flag_ok, msg_str, error_number, segmstr, a, b, lvcarea, bill, reservation, bediener, master, res_line, guest, htparam, counters, res_history, guest_pr, segment, reslin_queasy
        nonlocal pvilanguage, inp_resnr, resart, last_segm, curr_segm, gastnrherk, gastnrcom, gastnrpay, letterno, contact_nr, rechnerstart, rechnrend, res_mode, user_init, origin, groupname, comments, voucherno, bill_receiver, depositgef, limitdate, fixed_rate, init_rate, master_active, umsatz1, umsatz2, umsatz3, umsatz4, init_time, init_date
        nonlocal buff_bill


        nonlocal buff_bill

        i:int = 0
        b_list:int = 0

        segment = get_cache (Segment, {"segmentcode": [(eq, curr_segm)]})

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

            res_line = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"active_flag": [(le, 1)],"zipreis": [(gt, 0)]})

            if res_line:
                msg_str = translateExtended ("The selected COMPLIMENT segment is not valid:", lvcarea, "") + chr_unicode(10) + translateExtended ("Reservation record found with non-zero RmRate =", lvcarea, "") + " " + to_string(res_line.zipreis)
                error_number = 1

                return
        segmstr = entry(0, segment.bezeich, "$$0")


    def add_reslog(old_segm:int, new_segm:int):

        nonlocal flag_ok, msg_str, error_number, segmstr, a, b, lvcarea, bill, reservation, bediener, master, res_line, guest, htparam, counters, res_history, guest_pr, segment, reslin_queasy
        nonlocal pvilanguage, inp_resnr, resart, last_segm, curr_segm, gastnrherk, gastnrcom, gastnrpay, letterno, contact_nr, rechnerstart, rechnrend, res_mode, user_init, origin, groupname, comments, voucherno, bill_receiver, depositgef, limitdate, fixed_rate, init_rate, master_active, umsatz1, umsatz2, umsatz3, umsatz4, init_time, init_date
        nonlocal buff_bill


        nonlocal buff_bill

        cdate:date = get_current_date()
        heute:date = None
        zeit:int = 0
        segment1 = None
        Segment1 =  create_buffer("Segment1",Segment)

        res_line = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"active_flag": [(eq, 1)],"resstatus": [(eq, 6)]})

        if not res_line:

            if (reservation.bemerk  == (comments)):

                return

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == inp_resnr) & (Res_line.active_flag == 0) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5))).first()

            if not res_line:

                return
        heute = get_current_date()
        zeit = get_current_time_in_seconds()

        if reservation.mutdat != None:
            cdate = reservation.mutdat

        segment1 = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

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
            pass
            pass

        if reservation.bemerk  != (comments) :
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


            pass
            pass


    flag_ok, a, b = get_output(check_timebl(3, inp_resnr, None, "reservation", init_time, init_date))

    if not flag_ok:

        return generate_output()
    mk_mainres_go()

    return generate_output()