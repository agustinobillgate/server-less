#using conversion tools version: 1.0.0.117

# ============================================================
# Rulita 150825 | Added buffer_copy reservation.bestat_datum

# Rulita, 13-11-2025
# from Resline.kontakt_nr == reslinnr
# to Resline.kontakt_nr == Resline.reslinnr
# ============================================================
# Rd, 26/11/2025, with_for_update
# ============================================================
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.intevent_1 import intevent_1
from models import Reservation, Res_line, Reslin_queasy, Zinrstat, Master, Bediener, Res_history, Guest, History, Resplan, Zimkateg, Queasy
from sqlalchemy.orm.attributes import flag_modified

def reactivate1_1bl(resno:int, reslinno:int, user_init:string, all_flag:bool, deposit_flag:bool):

    prepare_cache ([Reservation, Res_line, Reslin_queasy, Zinrstat, Master, Bediener, Res_history, History, Resplan, Zimkateg, Queasy])

    new_resno = 0
    ci_date:date = None
    ci:date = None
    co:date = None
    priscilla_active:bool = True
    curr_resnr:int = 0
    curr_reslinnr:int = 0
    curr_ankunft:date = None
    reservation = res_line = reslin_queasy = zinrstat = master = bediener = res_history = guest = history = resplan = zimkateg = queasy = None

    t_reservation = t_resline = bresline = buf_rline = None

    T_reservation = create_buffer("T_reservation",Reservation)
    T_resline = create_buffer("T_resline",Res_line)
    Bresline = create_buffer("Bresline",Res_line)
    Buf_rline = create_buffer("Buf_rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_resno, ci_date, ci, co, priscilla_active, curr_resnr, curr_reslinnr, curr_ankunft, reservation, res_line, reslin_queasy, zinrstat, master, bediener, res_history, guest, history, resplan, zimkateg, queasy
        nonlocal resno, reslinno, user_init, all_flag, deposit_flag
        nonlocal t_reservation, t_resline, bresline, buf_rline


        nonlocal t_reservation, t_resline, bresline, buf_rline

        return {"new_resno": new_resno}

    def update_resline():

        nonlocal new_resno, ci_date, ci, co, priscilla_active, curr_resnr, curr_reslinnr, curr_ankunft, reservation, res_line, reslin_queasy, zinrstat, master, bediener, res_history, guest, history, resplan, zimkateg, queasy
        nonlocal resno, reslinno, user_init, all_flag, deposit_flag
        nonlocal t_reservation, t_resline, bresline, buf_rline


        nonlocal t_reservation, t_resline, bresline, buf_rline

        new_status:int = 0
        rbuff = None
        rline = None
        resline = None
        zinrbuff = None
        mbuff = None
        curr_ress:int = 0
        Rbuff =  create_buffer("Rbuff",Res_line)
        Rline =  create_buffer("Rline",Res_line)
        Resline =  create_buffer("Resline",Res_line)
        Zinrbuff =  create_buffer("Zinrbuff",Zinrstat)
        Mbuff =  create_buffer("Mbuff",Master)

        if res_line.resstatus == 9 and (res_line.betrieb_gastpay <= 2 or res_line.betrieb_gastpay == 5):

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "cancres")],"datum": [(eq, res_line.cancelled)]})

            if zinrstat:

                # zinrbuff = get_cache (Zinrstat, {"_recid": [(eq, zinrstat._recid)]})
                zinrbuff = db_session.query(Zinrstat).filter(Zinrstat._recid == zinrstat._recid).with_for_update().first()

                zinrbuff.zimmeranz = zinrbuff.zimmeranz - res_line.zimmeranz
                zinrbuff.personen = zinrbuff.personen -\
                        res_line.zimmeranz * res_line.erwachs


                pass
                pass

            if all_flag:

                for rbuff in db_session.query(Rbuff).filter(
                             (Rbuff.resnr == res_line.resnr) & (Rbuff.reslinnr != res_line.reslinnr) & (Rbuff.resstatus == 9) & ((res_line.betrieb_gastpay <= 2) | (res_line.betrieb_gastpay == 5))).order_by(Rbuff._recid).all():

                    zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "cancres")],"datum": [(eq, rbuff.cancelled)]})

                    if zinrstat:

                        # zinrbuff = get_cache (Zinrstat, {"_recid": [(eq, zinrstat._recid)]})
                        zinrbuff = db_session.query(Zinrstat).filter(Zinrstat._recid == zinrstat._recid).with_for_update().first()

                        zinrbuff.zimmeranz = zinrbuff.zimmeranz - rbuff.zimmeranz
                        zinrbuff.personen = zinrbuff.personen -\
                                rbuff.zimmeranz * rbuff.erwachs


                        pass
                        pass

        pass

        if (res_line.erwachs + res_line.kind1 + res_line.kind2) > 0:

            if res_line.betrieb_gastpay > 0:
                new_status = res_line.betrieb_gastpay
            else:
                new_status = 1
        else:
            new_status = 11
        curr_ress = res_line.resstatus
        curr_ankunft = res_line.ankunft

        if res_line.ankunft < ci_date:
            res_line.ankunft = ci_date

        if res_line.abreise <= res_line.ankunft:
            res_line.abreise = res_line.ankunft + timedelta(days=1)
        res_line.zinr = ""
        res_line.active_flag = 0
        res_line.resstatus = new_status
        res_line.changed = ci_date
        res_line.changed_id = user_init
        res_line.cancelled_id = ""
        res_line.betrieb_gastpay = curr_ress
        res_line.zimmer_wunsch = res_line.zimmer_wunsch + "$cancel;" + "$arrival$" + to_string(curr_ankunft, "99/99/9999") + ";"


        pass

        for resline in db_session.query(Resline).filter(
                     (Resline.resnr == res_line.resnr) & (Resline.l_zuordnung[inc_value(2)] == 1) & (Resline.kontakt_nr == res_line.reslinnr)).order_by(Resline._recid).with_for_update().all():
            curr_ress = resline.resstatus
            resline.active_flag = 0
            resline.resstatus = 11
            resline.ankunft = res_line.ankunft
            resline.abreise = res_line.abreise
            resline.zinr = ""
            resline.changed = ci_date
            resline.changed_id = user_init
            resline.cancelled_id = ""
            resline.betrieb_gastpay = curr_ress


            pass
        add_resplan(res_line._recid)

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if all_flag:

            for rbuff in db_session.query(Rbuff).filter(
                         (Rbuff.resnr == res_line.resnr) & (Rbuff.reslinnr != res_line.reslinnr) & ((Rbuff.resstatus == 9) | (Rbuff.resstatus == 10)) & (Rbuff.l_zuordnung[inc_value(2)] == 0)).order_by(Rbuff._recid).all():

                if priscilla_active:
                    get_output(intevent_1(12, rbuff.zinr, "Priscilla", rbuff.resnr, rbuff.reslinnr))

                # rline = get_cache (Res_line, {"_recid": [(eq, rbuff._recid)]})
                rline = db_session.query(Res_line).filter(Res_line._recid == rbuff._recid).with_for_update().first()

                if (rline.erwachs + rline.kind1 + rline.kind2) > 0:

                    if rline.betrieb_gastpay > 0:
                        new_status = rline.betrieb_gastpay
                    else:
                        new_status = 1
                else:
                    new_status = 11
                curr_ankunft = rline.ankunft


                curr_ress = rline.resstatus

                if rline.ankunft < ci_date:
                    rline.ankunft = ci_date

                if rline.abreise <= rline.ankunft:
                    rline.abreise = rline.ankunft + timedelta(days=1)
                rline.zinr = ""
                rline.active_flag = 0
                rline.resstatus = new_status
                rline.changed = ci_date
                rline.changed_id = user_init
                rline.cancelled_id = ""
                rline.betrieb_gastpay = curr_ress
                ci = rline.ankunf
                co = rline.abreise
                rline.zimmer_wunsch = rline.zimmer_wunsch + "$cancel;" + "$arrival$" + to_string(curr_ankunft, "99/99/9999") + ";"


                pass
                pass

                for resline in db_session.query(Resline).filter(
                             (Resline.resnr == rbuff.resnr) & (Resline.l_zuordnung[inc_value(2)] == 1) & (Resline.kontakt_nr == rbuff.reslinnr)).order_by(Resline._recid).with_for_update().all():
                    curr_ress = resline.resstatus

                    if priscilla_active:
                        get_output(intevent_1(12, resline.zinr, "Priscilla", resline.resnr, resline.reslinnr))
                    resline.active_flag = 0
                    resline.resstatus = 11
                    resline.ankunft = ci
                    resline.abreise = co
                    resline.zinr = ""
                    resline.changed = ci_date
                    resline.changed_id = user_init
                    resline.cancelled_id = ""
                    resline.betrieb_gastpay = curr_ress


                    pass
                
                add_resplan(rbuff._recid)
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.resnr = res_line.resnr
                res_history.reslinnr = res_line.reslinnr
                res_history.action = "RE-RES"


                res_history.aenderung = "Cancel Reservation with resno: " + to_string(rbuff.resnr) + "/" + to_string(rbuff.reslinnr, "999") + " and " + "Reactive All Reservation by UserID: " + user_init


        if reservation.activeflag == 1:
            pass
            reservation.activeflag = 0
            pass

        master = get_cache (Master, {"gastnr": [(eq, res_line.gastnr)],"resnr": [(eq, res_line.resnr)]})

        if master:

            # mbuff = get_cache (Master, {"_recid": [(eq, master._recid)]})
            mbuff = db_session.query(Master).filter(Master._recid == master._recid).with_for_update().first()
            mbuff.active = True
            pass
            pass

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        history = History()
        db_session.add(history)

        history.gastnr = res_line.gastnrmember
        history.ankunft = curr_ankunft
        history.abreise = get_current_date()
        history.zimmeranz = res_line.zimmeranz
        history.zikateg = zimkateg.kurzbez
        history.zinr = res_line.zinr
        history.erwachs = res_line.erwachs
        history.gratis = res_line.gratis
        history.zipreis =  to_decimal(res_line.zipreis)
        history.arrangement = res_line.arrangement
        history.gastinfo = res_line.name + " - " +\
                guest.adresse1 + ", " + guest.wohnort
        history.abreisezeit = to_string(get_current_time_in_seconds(), "HH:MM")
        history.segmentcode = reservation.segmentcode
        history.zi_wechsel = False
        history.resnr = res_line.resnr
        history.reslinnr = res_line.reslinnr
        history.bemerk = "Cancel Reservation and Reactive by" +\
                " " + user_init


        pass
        pass
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.resnr = res_line.resnr
        res_history.reslinnr = res_line.reslinnr
        res_history.action = "RE-RES"


        res_history.aenderung = "Cancel Reservation with resno: " + to_string(res_line.resnr) + "/" + to_string(res_line.reslinnr, "999") + " and " + "Reactive by UserID: " + user_init
        pass
        pass


    def add_resplan(rint:int):

        nonlocal new_resno, ci_date, ci, co, priscilla_active, curr_resnr, curr_reslinnr, curr_ankunft, reservation, res_line, reslin_queasy, zinrstat, master, bediener, res_history, guest, history, resplan, zimkateg, queasy
        nonlocal resno, reslinno, user_init, all_flag, deposit_flag
        nonlocal t_reservation, t_resline, bresline, buf_rline


        nonlocal t_reservation, t_resline, bresline, buf_rline

        curr_date:date = None
        i:int = 0
        tmpdate:date = None
        rline = None
        buffplan = None
        Rline =  create_buffer("Rline",Res_line)
        Buffplan =  create_buffer("Buffplan",Resplan)

        rline = get_cache (Res_line, {"_recid": [(eq, rint)]})
        i = rline.resstatus
        tmpdate = rline.abreise - timedelta(days=1)

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, rline.zikatnr)]})
        for curr_date in date_range(rline.ankunft,tmpdate) :

            resplan = get_cache (Resplan, {"zikatnr": [(eq, zimkateg.zikatnr)],"datum": [(eq, curr_date)]})

            if not resplan:
                resplan = Resplan()
                db_session.add(resplan)

                resplan.datum = curr_date
                resplan.zikatnr = zimkateg.zikatnr
                resplan.anzzim[i - 1] = rline.zimmeranz

            elif resplan:

                # buffplan = get_cache (Resplan, {"_recid": [(eq, resplan._recid)]})
                buffplan = db_session.query(Resplan).filter(Resplan._recid == resplan._recid).with_for_update().first()
                buffplan.anzzim[i - 1] = buffplan.anzzim[i - 1] + rline.zimmeranz
                pass
                pass
        flag_modified(buffplan, "anzzim")
        flag_modified(resplan, "anzzim")

    def update_queasy():

        nonlocal new_resno, ci_date, ci, co, priscilla_active, curr_resnr, curr_reslinnr, curr_ankunft, reservation, res_line, reslin_queasy, zinrstat, master, bediener, res_history, guest, history, resplan, zimkateg, queasy
        nonlocal resno, reslinno, user_init, all_flag, deposit_flag
        nonlocal t_reservation, t_resline, bresline, buf_rline


        nonlocal t_reservation, t_resline, bresline, buf_rline

        datum:date = None
        upto_date:date = None
        i:int = 0
        iftask:string = ""
        origcode:string = ""
        do_it:bool = False
        cat_flag:bool = False
        roomnr:int = 0
        qsy = None
        zbuff = None
        Qsy =  create_buffer("Qsy",Queasy)
        Zbuff =  create_buffer("Zbuff",Zimkateg)

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})
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

        if res_line.ankunft == res_line.abreise:
            upto_date = res_line.abreise
        else:
            upto_date = res_line.abreise - timedelta(days=1)


        for datum in date_range(res_line.ankunft,upto_date) :

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                # qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})
                qsy = db_session.query(Queasy).filter(Queasy._recid == queasy._recid).with_for_update().first()

                if qsy:
                    qsy.logi2 = True
                    pass
                    pass

            if origcode != "":

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    # qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})
                    qsy = db_session.query(Queasy).filter(Queasy._recid == queasy._recid).with_for_update().first()

                    if qsy:
                        qsy.logi2 = True
                        pass
                        pass


    def update_resline_copy():

        nonlocal new_resno, ci_date, ci, co, priscilla_active, curr_resnr, curr_reslinnr, curr_ankunft, reservation, res_line, reslin_queasy, zinrstat, master, bediener, res_history, guest, history, resplan, zimkateg, queasy
        nonlocal resno, reslinno, user_init, all_flag, deposit_flag
        nonlocal t_reservation, t_resline, bresline, buf_rline


        nonlocal t_reservation, t_resline, bresline, buf_rline

        new_status:int = 0
        rbuff = None
        rline = None
        resline = None
        zinrbuff = None
        mbuff = None
        curr_ress:int = 0
        Rbuff =  create_buffer("Rbuff",Res_line)
        Rline =  create_buffer("Rline",Res_line)
        Resline =  create_buffer("Resline",Res_line)
        Zinrbuff =  create_buffer("Zinrbuff",Zinrstat)
        Mbuff =  create_buffer("Mbuff",Master)
        pass

        if (bresline.erwachs + bresline.kind1 + bresline.kind2) > 0:

            if bresline.betrieb_gastpay > 0:
                new_status = bresline.betrieb_gastpay
            else:
                new_status = 1
        else:
            new_status = 11
        curr_ress = bresline.resstatus
        curr_ankunft = bresline.ankunft

        if bresline.ankunft < ci_date:
            bresline.ankunft = ci_date

        if bresline.abreise <= res_line.ankunft:
            bresline.abreise = res_line.ankunft + 1
        bresline.zinr = ""
        bresline.active_flag = 0
        bresline.resstatus = new_status
        bresline.changed = ci_date
        bresline.changed_id = user_init
        bresline.cancelled_id = ""
        bresline.betrieb_gastpay = curr_ress
        bresline.anztag = bresline.abreise - bresline.ankunft
        bresline.zimmer_wunsch = bresline.zimmer_wunsch + "$cancel;" + "$arrival$" + to_string(curr_ankunft, "99/99/9999") + ";"


        pass

        # Rulita, 13-11-2025
        # from Resline.kontakt_nr == reslinnr
        # to Resline.kontakt_nr == Resline.reslinnr
        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == resno) & (Resline.l_zuordnung[inc_value(2)] == 1) & (Resline.kontakt_nr == Resline.reslinnr)).order_by(Resline._recid).all():
            curr_ress = resline.resstatus
            t_resline = Res_line()
            db_session.add(t_resline)

            buffer_copy(resline, t_resline,except_fields=["resline.resnr"])

            if resline.ankunft < ci_date:
                t_resline.ankunft = ci_date

            if resline.abreise <= resline.ankunft:
                t_resline.abreise = resline.ankunft + timedelta(days=1)
            t_resline.resnr = new_resno
            t_resline.active_flag = 0
            t_resline.resstatus = 11
            t_resline.zinr = ""
            t_resline.changed = ci_date
            t_resline.changed_id = user_init
            t_resline.cancelled_id = ""
            t_resline.betrieb_gastpay = curr_ress
            t_resline.anztag = (t_resline.abreise - t_resline.ankunft).days


        add_resplan(bresline._recid)

        if all_flag:

            for rbuff in db_session.query(Rbuff).filter(
                     (Rbuff.resnr == resno) & (Rbuff.reslinnr != reslinno) & ((Rbuff.resstatus == 9) | (Rbuff.resstatus == 10)) & (Rbuff.l_zuordnung[inc_value(2)] == 0)).order_by(Rbuff._recid).all():
                t_resline = Res_line()
                db_session.add(t_resline)

                buffer_copy(rbuff, t_resline,except_fields=["rbuff.resnr"])
                t_resline.resnr = new_resno

                if priscilla_active:
                    get_output(intevent_1(12, rbuff.zinr, "Priscilla", new_resno, rbuff.reslinnr))

                if (t_resline.erwachs + t_resline.kind1 + t_resline.kind2) > 0:

                    if t_resline.betrieb_gastpay > 0:
                        new_status = t_resline.betrieb_gastpay
                    else:
                        new_status = 1
                else:
                    new_status = 11
                curr_ress = t_resline.resstatus
                curr_ankunft = t_resline.ankunft

                if t_resline.ankunft < ci_date:
                    t_resline.ankunft = ci_date

                if t_resline.abreise <= t_resline.ankunft:
                    t_resline.abreise = rbuff.ankunft + timedelta(days=1)
                t_resline.zinr = ""
                t_resline.active_flag = 0
                t_resline.resstatus = new_status
                t_resline.changed = ci_date
                t_resline.changed_id = user_init
                t_resline.cancelled_id = ""
                t_resline.betrieb_gastpay = curr_ress
                ci = t_resline.ankunf
                co = t_resline.abreise
                t_resline.anztag = (t_resline.abreise - t_resline.ankunft).days
                t_resline.zimmer_wunsch = t_resline.zimmer_wunsch + "$cancel;" + "$arrival$" + to_string(curr_ankunft, "99/99/9999") + ";"

                for resline in db_session.query(Resline).filter(
                         (Resline.resnr == rbuff.resnr) & (Resline.l_zuordnung[inc_value(2)] == 1) & (Resline.kontakt_nr == rbuff.reslinnr)).order_by(Resline._recid).all():
                    t_resline = Res_line()
                    db_session.add(t_resline)

                    buffer_copy(resline, t_resline,except_fields=["resline.resnr"])
                    t_resline.resnr = new_resno


                    curr_ress = resline.resstatus

                    if priscilla_active:
                        get_output(intevent_1(12, resline.zinr, "Priscilla", new_resno, resline.reslinnr))
                    t_resline.active_flag = 0
                    t_resline.resstatus = 11
                    t_resline.ankunft = ci
                    t_resline.abreise = co
                    t_resline.zinr = ""
                    t_resline.changed = ci_date
                    t_resline.changed_id = user_init
                    t_resline.cancelled_id = ""
                    t_resline.betrieb_gastpay = curr_ress
                    t_resline.anztag = (t_resline.abreise - t_resline.ankunft).days


                add_resplan(t_resline._recid)
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.resnr = bresline.resnr
                res_history.reslinnr = bresline.reslinnr
                res_history.action = "RE-RES"


                res_history.aenderung = "Cancel Reservation with resno: " + to_string(rbuff.resnr) + "/" + to_string(rbuff.reslinnr, "999") + " and " + "Reactive All Reservation by UserID: " + user_init + " with New resno:" + to_string(new_resno)


        master = get_cache (Master, {"gastnr": [(eq, bresline.gastnr)],"resnr": [(eq, resno)]})

        if master:

            # mbuff = get_cache (Master, {"_recid": [(eq, master._recid)]})
            mbuff = db_session.query(Master).filter(Master._recid == master._recid).with_for_update().first()
            mbuff.resnr = new_resno
            mbuff.active = True


            pass
            pass

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        guest = get_cache (Guest, {"gastnr": [(eq, bresline.gastnrmember)]})
        history = History()
        db_session.add(history)

        history.gastnr = bresline.gastnrmember
        history.ankunft = curr_ankunft
        history.abreise = get_current_date()
        history.zimmeranz = bresline.zimmeranz
        history.zikateg = zimkateg.kurzbez
        history.zinr = bresline.zinr
        history.erwachs = bresline.erwachs
        history.gratis = bresline.gratis
        history.zipreis =  to_decimal(bresline.zipreis)
        history.arrangement = bresline.arrangement
        history.gastinfo = bresline.name + " - " +\
                guest.adresse1 + ", " + guest.wohnort
        history.abreisezeit = to_string(get_current_time_in_seconds(), "HH:MM")
        history.segmentcode = reservation.segmentcode
        history.zi_wechsel = False
        history.resnr = bresline.resnr
        history.reslinnr = bresline.reslinnr


        history.bemerk = "Cancel Reservation and Reactive by" + " " + user_init
        pass
        pass
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.resnr = bresline.resnr
        res_history.reslinnr = bresline.reslinnr
        res_history.action = "RE-RES"


        res_history.aenderung = "Cancel Reservation with resno: " + to_string(bresline.resnr) + "/" + to_string(bresline.reslinnr, "999") + " and " + "Reactive by UserID: " + user_init + " with New resno:" + to_string(new_resno)


    def update_queasy_copy():

        nonlocal new_resno, ci_date, ci, co, priscilla_active, curr_resnr, curr_reslinnr, curr_ankunft, reservation, res_line, reslin_queasy, zinrstat, master, bediener, res_history, guest, history, resplan, zimkateg, queasy
        nonlocal resno, reslinno, user_init, all_flag, deposit_flag
        nonlocal t_reservation, t_resline, bresline, buf_rline


        nonlocal t_reservation, t_resline, bresline, buf_rline

        datum:date = None
        upto_date:date = None
        i:int = 0
        iftask:string = ""
        origcode:string = ""
        do_it:bool = False
        cat_flag:bool = False
        roomnr:int = 0
        qsy = None
        zbuff = None
        Qsy =  create_buffer("Qsy",Queasy)
        Zbuff =  create_buffer("Zbuff",Zimkateg)

        res_line = get_cache (Res_line, {"resnr": [(eq, new_resno)],"reslinnr": [(eq, reslinno)]})
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

        if res_line.ankunft == res_line.abreise:
            upto_date = res_line.abreise
        else:
            upto_date = res_line.abreise - timedelta(days=1)
        for datum in date_range(res_line.ankunft,upto_date) :

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                # qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})
                qsy = db_session.query(Queasy).filter(Queasy._recid == queasy._recid).with_for_update().first()

                if qsy:
                    qsy.logi2 = True
                    pass
                    pass

            if origcode != "":

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    # qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})
                    qsy = db_session.query(Queasy).filter(Queasy._recid == queasy._recid).with_for_update().first()

                    if qsy:
                        qsy.logi2 = True
                        pass
                        pass


    ci_date = get_output(htpdate(87))

    if deposit_flag:

        for reservation in db_session.query(Reservation).order_by(Reservation.resnr.desc()).yield_per(100):
            new_resno = reservation.resnr + 1


            break

        # reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})
        reservation = db_session.query(Reservation).filter(Reservation.resnr == resno).with_for_update().first()

        if reservation:
            t_reservation = Reservation()
            db_session.add(t_reservation)
            
            # Rulita | Added buffer_copy reservation.bestat_datum
            buffer_copy(reservation, t_reservation,except_fields=["reservation.resnr", "reservation.bestat_datum"])
            t_reservation.resnr = new_resno
            t_reservation.depositbez =  to_decimal("0")
            t_reservation.depositgef =  to_decimal("0")

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

        if res_line:
            t_resline = Res_line()
            db_session.add(t_resline)

            buffer_copy(res_line, t_resline,except_fields=["res_line.resnr"])
            t_resline.resnr = new_resno

        # bresline = get_cache (Res_line, {"resnr": [(eq, new_resno)]})
        bresline = db_session.query(Res_line).filter(
                     (Res_line.resnr == new_resno) & (Res_line.reslinnr == reslinno)).with_for_update().first()

        if bresline:

            if priscilla_active:
                get_output(intevent_1(12, bresline.zinr, "Priscilla", bresline.resnr, bresline.reslinnr))
            update_resline_copy()
            update_queasy_copy()

        if not all_flag:

            buf_rline = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

            if buf_rline:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "ResChanges"
                reslin_queasy.resnr = buf_rline.resnr
                reslin_queasy.reslinnr = buf_rline.reslinnr
                reslin_queasy.date2 = get_current_date()
                reslin_queasy.number2 = get_current_time_in_seconds()


                reslin_queasy.char3 = to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(buf_rline.name) + ";" + to_string("RE-ACTIVATE RSV") + ";" + to_string(" ") + ";" + to_string(" ") + ";"
                pass
                pass
        else:

            for buf_rline in db_session.query(Buf_rline).filter(
                     (Buf_rline.resnr == resno)).order_by(Buf_rline.reslinnr).all():
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "ResChanges"
                reslin_queasy.resnr = buf_rline.resnr
                reslin_queasy.reslinnr = buf_rline.reslinnr
                reslin_queasy.date2 = get_current_date()
                reslin_queasy.number2 = get_current_time_in_seconds()


                reslin_queasy.char3 = to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(buf_rline.name) + ";" + to_string("RE-ACTIVATE RSV") + ";" + to_string(" ") + ";" + to_string(" ") + ";"
                pass
                pass
    else:

        # res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})
        res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == resno) & (Res_line.reslinnr == reslinno)).with_for_update().first()

        if priscilla_active:
            get_output(intevent_1(12, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        # reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})
        reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == resno)).with_for_update().first()
        update_resline()
        update_queasy()

        if not all_flag:

            buf_rline = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

            if buf_rline:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "ResChanges"
                reslin_queasy.resnr = buf_rline.resnr
                reslin_queasy.reslinnr = buf_rline.reslinnr
                reslin_queasy.date2 = get_current_date()
                reslin_queasy.number2 = get_current_time_in_seconds()


                reslin_queasy.char3 = to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(buf_rline.name) + ";" + to_string("RE-ACTIVATE RSV") + ";" + to_string(" ") + ";" + to_string(" ") + ";"
                pass
                pass
        else:

            for buf_rline in db_session.query(Buf_rline).filter(
                     (Buf_rline.resnr == resno)).order_by(Buf_rline.reslinnr).all():
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "ResChanges"
                reslin_queasy.resnr = buf_rline.resnr
                reslin_queasy.reslinnr = buf_rline.reslinnr
                reslin_queasy.date2 = get_current_date()
                reslin_queasy.number2 = get_current_time_in_seconds()


                reslin_queasy.char3 = to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(buf_rline.name) + ";" + to_string("RE-ACTIVATE RSV") + ";" + to_string(" ") + ";" + to_string(" ") + ";"
                pass
                pass

    return generate_output()