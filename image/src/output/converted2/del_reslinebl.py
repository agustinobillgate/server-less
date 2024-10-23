from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.intevent_1 import intevent_1
from models import Queasy, Zimkateg, Res_line, Htparam, Reslin_queasy, Zinrstat, Outorder, Reservation, Guest, Bill, Master, Mast_art, Bediener, Res_history, Zimmer, Zimplan, Resplan

def del_reslinebl(pvilanguage:int, res_mode:str, resnr:int, reslinnr:int, user_init:str, cancel_str:str):
    del_mainres = False
    msg_str = ""
    ci_date:date = None
    name1:str = ""
    datum:date = None
    upto_date:date = None
    i:int = 0
    iftask:str = ""
    origcode:str = ""
    do_it:bool = False
    cat_flag:bool = False
    roomnr:int = 0
    priscilla_active:bool = True
    lvcarea:str = "del-resline"
    queasy = zimkateg = res_line = htparam = reslin_queasy = zinrstat = outorder = reservation = guest = bill = master = mast_art = bediener = res_history = zimmer = zimplan = resplan = None

    qsy = zbuff = rline = None

    Qsy = create_buffer("Qsy",Queasy)
    Zbuff = create_buffer("Zbuff",Zimkateg)
    Rline = create_buffer("Rline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal del_mainres, msg_str, ci_date, name1, datum, upto_date, i, iftask, origcode, do_it, cat_flag, roomnr, priscilla_active, lvcarea, queasy, zimkateg, res_line, htparam, reslin_queasy, zinrstat, outorder, reservation, guest, bill, master, mast_art, bediener, res_history, zimmer, zimplan, resplan
        nonlocal pvilanguage, res_mode, resnr, reslinnr, user_init, cancel_str
        nonlocal qsy, zbuff, rline


        nonlocal qsy, zbuff, rline
        return {"del_mainres": del_mainres, "msg_str": msg_str}

    def release_zinr(new_zinr:str):

        nonlocal del_mainres, msg_str, ci_date, name1, datum, upto_date, i, iftask, origcode, do_it, cat_flag, roomnr, priscilla_active, lvcarea, queasy, zimkateg, res_line, htparam, reslin_queasy, zinrstat, outorder, reservation, guest, bill, master, mast_art, bediener, res_history, zimmer, zimplan, resplan
        nonlocal pvilanguage, res_mode, resnr, reslinnr, user_init, cancel_str
        nonlocal qsy, zbuff, rline


        nonlocal qsy, zbuff, rline

        res_recid1:int = 0
        res_line1 = None
        res_line2 = None
        rline = None
        beg_datum:date = None
        answer:bool = False
        parent_nr:int = 0
        Res_line1 =  create_buffer("Res_line1",Res_line)
        Res_line2 =  create_buffer("Res_line2",Res_line)
        Rline =  create_buffer("Rline",Res_line)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 87)).first()

        rline = db_session.query(Rline).filter(
                 (Rline.resnr == resnr) & (Rline.reslinnr == reslinnr)).first()

        if rline.zinr != "":
            beg_datum = rline.ankunft
            res_recid1 = 0

            if res_mode.lower()  == ("delete").lower()  or res_mode.lower()  == ("cancel").lower()  and rline.resstatus == 1:

                res_line1 = db_session.query(Res_line1).filter(
                         (Res_line1.resnr == resnr) & (Res_line1.zinr == rline.zinr) & (Res_line1.resstatus == 11)).first()

                if res_line1:
                    res_line1.resstatus = 1
                    res_recid1 = res_line1._recid

        if res_mode.lower()  == ("inhouse").lower() :
            answer = True
            beg_datum = htparam.fdate

            if rline.resstatus == 6 and (rline.zinr.lower()  != (new_zinr).lower()):

                res_line1 = db_session.query(Res_line1).filter(
                         (Res_line1.resnr == resnr) & (Res_line1.zinr == rline.zinr) & (Res_line1.resstatus == 13)).first()

                if res_line1:

                    for res_line2 in db_session.query(Res_line2).filter(
                             (Res_line2.resnr == resnr) & (Res_line2.zinr == rline.zinr) & (Res_line2.resstatus == 13)).order_by(Res_line2._recid).all():

                        bill = db_session.query(Bill).filter(
                                 (Bill.resnr == resnr) & (Bill.reslinnr == res_line2.reslinnr) & (Bill.flag == 0) & (Bill.zinr == res_line2.zinr)).first()
                        bill.zinr = new_zinr
                        parent_nr = bill.parent_nr

                        for bill in db_session.query(Bill).filter(
                                 (Bill.resnr == resnr) & (Bill.parent_nr == parent_nr) & (Bill.flag == 0) & (Bill.zinr == res_line2.zinr)).order_by(Bill._recid).all():
                            bill.zinr = new_zinr
                            pass
                        res_line2.zinr = new_zinr
                        pass

                    zimmer = db_session.query(Zimmer).filter(
                             (Zimmer.zinr == rline.zinr)).first()
                    zimmer.zistatus = 2


    def min_resplan():

        nonlocal del_mainres, msg_str, ci_date, name1, datum, upto_date, iftask, origcode, do_it, cat_flag, roomnr, priscilla_active, lvcarea, queasy, zimkateg, res_line, htparam, reslin_queasy, zinrstat, outorder, reservation, guest, bill, master, mast_art, bediener, res_history, zimmer, zimplan, resplan
        nonlocal pvilanguage, res_mode, resnr, reslinnr, user_init, cancel_str
        nonlocal qsy, zbuff, rline


        nonlocal qsy, zbuff, rline

        curr_date:date = None
        beg_datum:date = None
        i:int = 0
        rline = None
        Rline =  create_buffer("Rline",Res_line)

        rline = db_session.query(Rline).filter(
                 (Rline.resnr == resnr) & (Rline.reslinnr == reslinnr)).first()

        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.zinr == rline.zinr)).first()

        if zimmer and (not zimmer.sleeping):
            pass
        else:
            i = rline.resstatus

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == rline.zikatnr)).first()

            if res_mode.lower()  == ("inhouse").lower() :
                beg_datum = get_current_date()
            else:
                beg_datum = rline.ankunft
            curr_date = beg_datum
            while curr_date >= beg_datum and curr_date < rline.abreise:

                resplan = db_session.query(Resplan).filter(
                         (Resplan.zikatnr == zimkateg.zikatnr) & (Resplan.datum == curr_date)).first()

                if resplan:
                    resplan.anzzim[i - 1] = resplan.anzzim[i - 1] - rline.zimmeranz
                pass
                curr_date = curr_date + timedelta(days=1)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if (res_mode.lower()  == ("cancel").lower()  or res_mode.lower()  == ("delete").lower()):

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = res_line.resnr
        reslin_queasy.reslinnr = res_line.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(res_line.name) + ";" + to_string(cancel_str) + ";" + to_string(" ") + ";" + to_string(" ") + ";"
        pass
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(iftask, 0, 10) == ("$origcode$").lower() :
                origcode = substring(iftask, 10)
                break

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 152)).first()

    if queasy:
        cat_flag = True

    zbuff = db_session.query(Zbuff).filter(
             (Zbuff.zikatnr == res_line.zikatnr)).first()

    if zbuff:

        if cat_flag:
            roomnr = zbuff.typ
        else:
            roomnr = zbuff.zikatnr

    if res_line.ankunft == res_line.abreise:
        upto_date = res_line.abreise
    else:
        upto_date = res_line.abreise - timedelta(days=1)
    for datum in date_range(res_line.ankunft,upto_date) :

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 171) & (Queasy.date1 == datum) & (Queasy.number1 == roomnr) & (Queasy.char1 == "")).first()

        if queasy and queasy.logi1 == False and queasy.logi2 == False:
            queasy.logi2 = True
            pass

        if origcode != "":

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.date1 == datum) & (Queasy.number1 == roomnr) & (func.lower(Queasy.char1) == (origcode).lower())).first()

            if queasy and queasy.logi1 == False and queasy.logi2 == False:
                queasy.logi2 = True
                pass
    name1 = res_line.name

    if res_line.zinr != "":

        rline = db_session.query(Rline).filter(
                 (Rline.active_flag == 0) & (func.lower(Rline.memozinr).op("~")((("*;*").lower().replace("*",".*")))) & (entry(1, Rline.memozinr, ";") == res_line.zinr) & (not Rline.ankunft >= res_line.abreise) & (not Rline.abreise <= res_line.ankunft) & (Rline.resnr != res_line.resnr) & (Rline.zinr != res_line.zinr)).first()

        if not rline:

            rline = db_session.query(Rline).filter(
                     (Rline.active_flag == 1) & (func.lower(Rline.memozinr).op("~")((("*;*").lower().replace("*",".*")))) & (entry(1, Rline.memozinr, ";") == res_line.zinr) & (Rline.resnr != res_line.resnr) & (Rline.zinr != res_line.zinr)).first()

        if rline:
            msg_str = msg_str + chr(2) + "&W" + "Reservation found with Memo RmNo =" + " " + res_line.zinr

    if (res_mode.lower()  == ("cancel").lower()) and (res_line.resstatus <= 2 or res_line.resstatus == 5):

        zinrstat = db_session.query(Zinrstat).filter(
                 (func.lower(Zinrstat.zinr) == ("CancRes").lower()) & (Zinrstat.datum == ci_date)).first()

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = ci_date
            zinrstat.zinr = "CancRes"


        zinrstat.zimmeranz = zinrstat.zimmeranz + res_line.zimmeranz
        zinrstat.personen = zinrstat.personen + res_line.zimmeranz * res_line.erwachs

    if (res_line.resstatus <= 2 or res_line.resstatus == 5) and res_line.zinr != "":

        outorder = db_session.query(Outorder).filter(
                 (Outorder.zinr == res_line.zinr) & (Outorder.betriebsnr == res_line.resnr)).first()

        if outorder:
            db_session.delete(outorder)
            pass
    release_zinr(res_line.zinr)
    min_resplan()

    if res_mode.lower()  == ("delete").lower() :

        if priscilla_active:
            get_output(intevent_1(15, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))
        res_line.betrieb_gastpay = res_line.resstatus
        res_line.resstatus = 99
        res_line.active_flag = 2
        res_line.cancelled = ci_date
        res_line.cancelled_id = user_init +\
                ";" + to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS") +\
                ";" + res_line.zinr
        res_line.zinr = ""

        for rline in db_session.query(Rline).filter(
                 (Rline.resnr == res_line.resnr) & (Rline.l_zuordnung[inc_value(2)] == 1) & (Rline.kontakt_nr == reslinnr)).order_by(Rline._recid).all():
            rline.zinr = ""
            rline.betrieb_gastpay = rline.resstatus
            rline.resstatus = 99
            rline.active_flag = 2
            rline.cancelled = ci_date
            rline.cancelled_id = user_init +\
                    ";" + to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS")


            pass

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == resnr)).first()

        if reservation:
            reservation.vesrdepot2 = cancel_str


    else:

        if priscilla_active:
            get_output(intevent_1(14, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))
        res_line.betrieb_gastpay = res_line.resstatus
        res_line.resstatus = 9
        res_line.active_flag = 2
        res_line.cancelled = ci_date
        res_line.cancelled_id = user_init +\
                ";" + to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS") +\
                ";" + res_line.zinr
        res_line.zinr = ""

        for rline in db_session.query(Rline).filter(
                 (Rline.resnr == res_line.resnr) & (Rline.l_zuordnung[inc_value(2)] == 1) & (Rline.kontakt_nr == reslinnr)).order_by(Rline._recid).all():
            rline.zinr = ""
            rline.betrieb_gastpay = rline.resstatus
            rline.resstatus = 9
            rline.active_flag = 2
            rline.cancelled = ci_date
            rline.cancelled_id = user_init +\
                    ";" + to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS")


            pass

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == resnr)).first()

        if reservation:
            reservation.vesrdepot2 = cancel_str

    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & (Res_line.resstatus != 9) & (Res_line.resstatus != 99)).first()

    if not res_line:
        del_mainres = True

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == resnr)).first()
        reservation.activeflag = 1

        if cancel_str != "":
            reservation.vesrdepot2 = cancel_str

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == reservation.gastnr)).first()
        guest.stornos = guest.stornos + 1

    bill = db_session.query(Bill).filter(
             (Bill.resnr == resnr) & (Bill.reslinnr == 0) & (Bill.zinr == "")).first()

    if bill:
        db_session.delete(bill)
        pass

    master = db_session.query(Master).filter(
             (Master.resnr == resnr) & (Master.flag == 0)).first()

    if master:
        db_session.delete(master)
        pass

    for mast_art in db_session.query(Mast_art).filter(
             (Mast_art.resnr == resnr) & (Mast_art.reslinnr == 1)).order_by(Mast_art._recid).all():
        db_session.delete(mast_art)

    if res_mode.lower()  == ("delete").lower() :

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = ci_date
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Delete ResLine: ResNo " + to_string(resnr) + " No " +\
                to_string(reslinnr) + " - " + name1
        res_history.action = "Reservation"


        pass

    for zimplan in db_session.query(Zimplan).filter(
                 (Zimplan.zinr == rline.zinr) & (Zimplan.datum >= beg_datum) & (Zimplan.datum < rline.abreise)).order_by(Zimplan._recid).all():

        if res_recid1 != 0:
            zimplan.res_recid = res_recid1
        else:
            db_session.delete(zimplan)
        pass

    return generate_output()