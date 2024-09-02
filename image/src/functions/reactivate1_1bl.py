from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.intevent_1 import intevent_1
from sqlalchemy import func
from models import Reservation, Res_line, Bresline, Reslin_queasy, Zinrstat, Master, Bediener, Guest, History, Res_history, Resplan, Zimkateg, Queasy

def reactivate1_1bl(resno:int, reslinno:int, user_init:str, all_flag:bool, deposit_flag:bool):
    new_resno = 0
    ci_date:date = None
    ci:date = None
    co:date = None
    priscilla_active:bool = True
    curr_resnr:int = 0
    curr_reslinnr:int = 0
    curr_ankunft:date = None
    reservation = res_line = bresline = reslin_queasy = zinrstat = master = bediener = guest = history = res_history = resplan = zimkateg = queasy = None

    t_reservation = t_resline = bresline = buf_rline = rbuff = rline = resline = zinrbuff = mbuff = buffplan = qsy = zbuff = None

    T_reservation = Reservation
    T_resline = Res_line
    Bresline = Res_line
    Buf_rline = Res_line
    Rbuff = Res_line
    Rline = Res_line
    Resline = Res_line
    Zinrbuff = Zinrstat
    Mbuff = Master
    Buffplan = Resplan
    Qsy = Queasy
    Zbuff = Zimkateg

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_resno, ci_date, ci, co, priscilla_active, curr_resnr, curr_reslinnr, curr_ankunft, reservation, res_line, bresline, reslin_queasy, zinrstat, master, bediener, guest, history, res_history, resplan, zimkateg, queasy
        nonlocal t_reservation, t_resline, bresline, buf_rline, rbuff, rline, resline, zinrbuff, mbuff, buffplan, qsy, zbuff


        nonlocal t_reservation, t_resline, bresline, buf_rline, rbuff, rline, resline, zinrbuff, mbuff, buffplan, qsy, zbuff
        return {"new_resno": new_resno}

    def update_resline():

        nonlocal new_resno, ci_date, ci, co, priscilla_active, curr_resnr, curr_reslinnr, curr_ankunft, reservation, res_line, bresline, reslin_queasy, zinrstat, master, bediener, guest, history, res_history, resplan, zimkateg, queasy
        nonlocal t_reservation, t_resline, bresline, buf_rline, rbuff, rline, resline, zinrbuff, mbuff, buffplan, qsy, zbuff


        nonlocal t_reservation, t_resline, bresline, buf_rline, rbuff, rline, resline, zinrbuff, mbuff, buffplan, qsy, zbuff

        new_status:int = 0
        Rbuff = Res_line
        Rline = Res_line
        Resline = Res_line
        Zinrbuff = Zinrstat
        Mbuff = Master

        if res_line.resstatus == 9 and (res_line.betrieb_gastpay <= 2 or res_line.betrieb_gastpay == 5):

            zinrstat = db_session.query(Zinrstat).filter(
                        (func.lower(Zinrstat.zinr) == "CancRes") &  (Zinrstat.datum == res_line.CANCELLED)).first()

            if zinrstat:

                zinrbuff = db_session.query(Zinrbuff).filter(
                            (Zinrbuff._recid == zinrstat._recid)).first()
                zinrbuff.zimmeranz = zinrbuff.zimmeranz - res_line.zimmeranz
                zinrbuff.personen = zinrbuff.personen -\
                        res_line.zimmeranz * res_line.erwachs

                zinrbuff = db_session.query(Zinrbuff).first()


            if all_flag:

                for rbuff in db_session.query(Rbuff).filter(
                            (Rbuff.resnr == res_line.resnr) &  (Rbuff.reslinnr != res_line.reslinnr) &  (Rbuff.resstatus == 9) &  ((res_line.betrieb_gastpay <= 2) |  (res_line.betrieb_gastpay == 5))).all():

                    zinrstat = db_session.query(Zinrstat).filter(
                                (func.lower(Zinrstat.zinr) == "CancRes") &  (Zinrstat.datum == rbuff.CANCELLED)).first()

                    if zinrstat:

                        zinrbuff = db_session.query(Zinrbuff).filter(
                                    (Zinrbuff._recid == zinrstat._recid)).first()
                        zinrbuff.zimmeranz = zinrbuff.zimmeranz - rbuff.zimmeranz
                        zinrbuff.personen = zinrbuff.personen -\
                                rbuff.zimmeranz * rbuff.erwachs

                        zinrbuff = db_session.query(Zinrbuff).first()

        res_line = db_session.query(Res_line).first()

        if (res_line.erwachs + res_line.kind1 + res_line.kind2) > 0:

            if res_line.betrieb_gastpay > 0:
                new_status = res_line.betrieb_gastpay
            else:
                new_status = 1
        else:
            new_status = 11
        curr_ankunft = res_line.ankunft

        if res_line.ankunft < ci_date:
            res_line.ankunft = ci_date

        if res_line.abreise <= res_line.ankunft:
            res_line.abreise = res_line.ankunft + 1
        res_line.zinr = ""
        res_line.active_flag = 0
        res_line.resstatus = new_status
        res_line.changed = ci_date
        res_line.changed_id = user_init
        res_line.cancelled_id = ""
        res_line.betrieb_gastpay = 9
        res_line.zimmer_wunsch = res_line.zimmer_wunsch + "$cancel;" + "$arrival$" + to_string(curr_ankunft, "99/99/9999") + ";"

        res_line = db_session.query(Res_line).first()

        for resline in db_session.query(Resline).filter(
                    (Resline.resnr == res_line.resnr) &  (Resline.l_zuordnung[2] == 1) &  (Resline.kontakt_nr == res_line.reslinnr)).all():
            resline.active_flag = 0
            resline.resstatus = 11
            resline.ankunft = res_line.ankunft
            resline.abreise = res_line.abreise
            resline.zinr = ""
            resline.changed = ci_date
            resline.changed_id = user_init
            resline.cancelled_id = ""
            resline.betrieb_gastpay = 9

        add_resplan(res_line._recid)

        if all_flag:

            for rbuff in db_session.query(Rbuff).filter(
                        (Rbuff.resnr == res_line.resnr) &  (Rbuff.reslinnr != res_line.reslinnr) &  ((Rbuff.resstatus == 9) |  (Rbuff.resstatus == 10)) &  (Rbuff.l_zuordnung[2] == 0)).all():

                if priscilla_active:
                    get_output(intevent_1(12, rbuff.zinr, "Priscilla", rbuff.resnr, rbuff.reslinnr))

                rline = db_session.query(Rline).filter(
                            (Rline._recid == rbuff._recid)).first()

                if (rline.erwachs + rline.kind1 + rline.kind2) > 0:

                    if rline.betrieb_gastpay > 0:
                        new_status = rline.betrieb_gastpay
                    else:
                        new_status = 1
                else:
                    new_status = 11
                curr_ankunft = rline.ankunft

                if rline.ankunft < ci_date:
                    rline.ankunft = ci_date

                if rline.abreise <= rline.ankunft:
                    rline.abreise = rline.ankunft + 1
                rline.zinr = ""
                rline.active_flag = 0
                rline.resstatus = new_status
                rline.changed = ci_date
                rline.changed_id = user_init
                rline.cancelled_id = ""
                rline.betrieb_gastpay = 9
                ci = rline.ankunf
                co = rline.abreise
                rline.zimmer_wunsch = rline.zimmer_wunsch + "$cancel;" + "$arrival$" + to_string(curr_ankunft, "99/99/9999") + ";"

                rline = db_session.query(Rline).first()


                for resline in db_session.query(Resline).filter(
                            (Resline.resnr == rbuff.resnr) &  (Resline.l_zuordnung[2] == 1) &  (Resline.kontakt_nr == rbuff.reslinnr)).all():

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
                    resline.betrieb_gastpay = 9

                add_resplan(rbuff._recid)


        if reservation.activeflag == 1:

            reservation = db_session.query(Reservation).first()
            reservation.activeflag = 0

            reservation = db_session.query(Reservation).first()

        master = db_session.query(Master).filter(
                    (Master.gastnr == res_line.gastnr) &  (Master.resnr == res_line.resnr)).first()

        if master:

            mbuff = db_session.query(Mbuff).filter(
                        (Mbuff._recid == master._recid)).first()
            mbuff.active = True

            mbuff = db_session.query(Mbuff).first()


        bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()

        guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()
        history = History()
        db_session.add(history)

        history.gastnr = res_line.gastnrmember
        history.ankunft = res_line.ankunft
        history.abreise = get_current_date()
        history.zimmeranz = res_line.zimmeranz
        history.zikateg = zimkateg.kurzbez
        history.zinr = res_line.zinr
        history.erwachs = res_line.erwachs
        history.gratis = res_line.gratis
        history.zipreis = res_line.zipreis
        history.arrangement = res_line.arrangement
        history.gastinfo = res_line.name + " - " +\
                guest.adresse1 + ", " + guest.wohnort
        history.abreisezeit = to_string(get_current_time_in_seconds(), "HH:MM")
        history.segmentcode = reservation.segmentcode
        history.zi_wechsel = False
        history.resnr = res_line.resnr
        history.reslinnr = res_line.reslinnr


        history.bemerk = "Cancel Reservation and Reactive by" + " " + user_init

        history = db_session.query(History).first()

        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.resnr = res_line.resnr
        res_history.reslinnr = res_line.reslinnr
        res_history.action = "RE_RES"


        res_history.aenderung = "Cancel Reservation and Reactive by" + " " + user_init


    def add_resplan(rint:int):

        nonlocal new_resno, ci_date, ci, co, priscilla_active, curr_resnr, curr_reslinnr, curr_ankunft, reservation, res_line, bresline, reslin_queasy, zinrstat, master, bediener, guest, history, res_history, resplan, zimkateg, queasy
        nonlocal t_reservation, t_resline, bresline, buf_rline, rbuff, rline, resline, zinrbuff, mbuff, buffplan, qsy, zbuff


        nonlocal t_reservation, t_resline, bresline, buf_rline, rbuff, rline, resline, zinrbuff, mbuff, buffplan, qsy, zbuff

        curr_date:date = None
        i:int = 0
        Rline = Res_line
        Buffplan = Resplan

        rline = db_session.query(Rline).filter(
                (Rline._recid == rint)).first()
        i = rline.resstatus

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == rline.zikatnr)).first()
        for curr_date in range(rline.ankunft,(rline.abreise - 1)  + 1) :

            resplan = db_session.query(Resplan).filter(
                    (Resplan.zikatnr == zimkateg.zikatnr) &  (Resplan.datum == curr_date)).first()

            if not resplan:
                resplan = Resplan()
                db_session.add(resplan)

                resplan.datum = curr_date
                resplan.zikatnr = zimkateg.zikatnr
                resplan.anzzim[i - 1] = rline.zimmeranz

            elif resplan:

                buffplan = db_session.query(Buffplan).filter(
                        (Buffplan._recid == resplan._recid)).first()
                buffplan.anzzim[i - 1] = buffplan.anzzim[i - 1] + rline.zimmeranz

                buffplan = db_session.query(Buffplan).first()


    def update_queasy():

        nonlocal new_resno, ci_date, ci, co, priscilla_active, curr_resnr, curr_reslinnr, curr_ankunft, reservation, res_line, bresline, reslin_queasy, zinrstat, master, bediener, guest, history, res_history, resplan, zimkateg, queasy
        nonlocal t_reservation, t_resline, bresline, buf_rline, rbuff, rline, resline, zinrbuff, mbuff, buffplan, qsy, zbuff


        nonlocal t_reservation, t_resline, bresline, buf_rline, rbuff, rline, resline, zinrbuff, mbuff, buffplan, qsy, zbuff

        datum:date = None
        upto_date:date = None
        i:int = 0
        iftask:str = ""
        origcode:str = ""
        do_it:bool = False
        cat_flag:bool = False
        roomnr:int = 0
        Qsy = Queasy
        Zbuff = Zimkateg

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(iftask, 0, 10) == "$origcode$":
                origcode = substring(iftask, 10)
                return

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
            upto_date = res_line.abreise - 1
        for datum in range(res_line.ankunft,upto_date + 1) :

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 171) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (Queasy.char1 == "")).first()

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()

                if qsy:
                    qsy.logi2 = True

                    qsy = db_session.query(Qsy).first()


            if origcode != "":

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 171) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (func.lower(Queasy.char1) == (origcode).lower())).first()

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    qsy = db_session.query(Qsy).filter(
                            (Qsy._recid == queasy._recid)).first()

                    if qsy:
                        qsy.logi2 = True

                        qsy = db_session.query(Qsy).first()


    def update_resline_copy():

        nonlocal new_resno, ci_date, ci, co, priscilla_active, curr_resnr, curr_reslinnr, curr_ankunft, reservation, res_line, bresline, reslin_queasy, zinrstat, master, bediener, guest, history, res_history, resplan, zimkateg, queasy
        nonlocal t_reservation, t_resline, bresline, buf_rline, rbuff, rline, resline, zinrbuff, mbuff, buffplan, qsy, zbuff


        nonlocal t_reservation, t_resline, bresline, buf_rline, rbuff, rline, resline, zinrbuff, mbuff, buffplan, qsy, zbuff

        new_status:int = 0
        Rbuff = Res_line
        Rline = Res_line
        Resline = Res_line
        Zinrbuff = Zinrstat
        Mbuff = Master

        bresline = db_session.query(Bresline).first()

        if (bresline.erwachs + bresline.kind1 + bresline.kind2) > 0:

            if bresline.betrieb_gastpay > 0:
                new_status = bresline.betrieb_gastpay
            else:
                new_status = 1
        else:
            new_status = 11
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
        bresline.betrieb_gastpay = 9
        bresline.anztag = bresline.abreise - bresline.ankunft
        bresline.zimmer_wunsch = bresline.zimmer_wunsch + "$cancel;" + "$arrival$" + to_string(curr_ankunft, "99/99/9999") + ";"

        bresline = db_session.query(Bresline).first()

        for resline in db_session.query(Resline).filter(
                (Resline.resnr == resno) &  (Resline.l_zuordnung[2] == 1) &  (Resline.kontakt_nr == reslinnr)).all():
            t_resline = T_resline()
            db_session.add(t_resline)

            buffer_copy(resline, t_resline,except_fields=["resline.resnr"])

            if resline.ankunft < ci_date:
                t_resline.ankunft = ci_date

            if resline.abreise <= resline.ankunft:
                t_resline.abreise = resline.ankunft + 1
            t_resline.resnr = new_resno
            t_resline.active_flag = 0
            t_resline.resstatus = 11
            t_resline.zinr = ""
            t_resline.changed = ci_date
            t_resline.changed_id = user_init
            t_resline.cancelled_id = ""
            t_resline.betrieb_gastpay = 9
            t_resline.anztag = t_resline.abreise - t_resline.ankunft


        add_resplan(bresline._recid)

        if all_flag:

            for rbuff in db_session.query(Rbuff).filter(
                    (Rbuff.resnr == resno) &  (Rbuff.reslinnr != reslinno) &  ((Rbuff.resstatus == 9) |  (Rbuff.resstatus == 10)) &  (Rbuff.l_zuordnung[2] == 0)).all():
                t_resline = T_resline()
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
                curr_ankunft = t_resline.ankunft

                if t_resline.ankunft < ci_date:
                    t_resline.ankunft = ci_date

                if t_resline.abreise <= t_resline.ankunft:
                    t_resline.abreise = rbuff.ankunft + 1
                t_resline.zinr = ""
                t_resline.active_flag = 0
                t_resline.resstatus = new_status
                t_resline.changed = ci_date
                t_resline.changed_id = user_init
                t_resline.cancelled_id = ""
                t_resline.betrieb_gastpay = 9
                ci = t_resline.ankunf
                co = t_resline.abreise
                t_resline.anztag = t_resline.abreise - t_resline.ankunft
                t_resline.zimmer_wunsch = t_resline.zimmer_wunsch + "$cancel;" + "$arrival$" + to_string(curr_ankunft, "99/99/9999") + ";"

                for resline in db_session.query(Resline).filter(
                        (Resline.resnr == rbuff.resnr) &  (Resline.l_zuordnung[2] == 1) &  (Resline.kontakt_nr == rbuff.reslinnr)).all():
                    t_resline = T_resline()
                    db_session.add(t_resline)

                    buffer_copy(resline, t_resline,except_fields=["resline.resnr"])
                    t_resline.resnr = new_resno

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
                    t_resline.betrieb_gastpay = 9
                    t_resline.anztag = t_resline.abreise - t_resline.ankunft


                add_resplan(t_resline._recid)


        master = db_session.query(Master).filter(
                (Master.gastnr == bresline.gastnr) &  (Master.resnr == resno)).first()

        if master:

            mbuff = db_session.query(Mbuff).filter(
                    (Mbuff._recid == master._recid)).first()
            mbuff.resnr = new_resno
            mbuff.active = True

            mbuff = db_session.query(Mbuff).first()


        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == bresline.gastnrmember)).first()
        history = History()
        db_session.add(history)

        history.gastnr = bresline.gastnrmember
        history.ankunft = bresline.ankunft
        history.abreise = get_current_date()
        history.zimmeranz = bresline.zimmeranz
        history.zikateg = zimkateg.kurzbez
        history.zinr = bresline.zinr
        history.erwachs = bresline.erwachs
        history.gratis = bresline.gratis
        history.zipreis = bresline.zipreis
        history.arrangement = bresline.arrangement
        history.gastinfo = bresline.name + " - " +\
                guest.adresse1 + ", " + guest.wohnort
        history.abreisezeit = to_string(get_current_time_in_seconds(), "HH:MM")
        history.segmentcode = reservation.segmentcode
        history.zi_wechsel = False
        history.resnr = bresline.resnr
        history.reslinnr = bresline.reslinnr


        history.bemerk = "Cancel Reservation and Reactive by" + " " + user_init

        history = db_session.query(History).first()

        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.resnr = bresline.resnr
        res_history.reslinnr = bresline.reslinnr
        res_history.action = "RE_RES"


        res_history.aenderung = "Cancel Reservation and Reactive by" + " " + user_init

    def update_queasy_copy():

        nonlocal new_resno, ci_date, ci, co, priscilla_active, curr_resnr, curr_reslinnr, curr_ankunft, reservation, res_line, bresline, reslin_queasy, zinrstat, master, bediener, guest, history, res_history, resplan, zimkateg, queasy
        nonlocal t_reservation, t_resline, bresline, buf_rline, rbuff, rline, resline, zinrbuff, mbuff, buffplan, qsy, zbuff


        nonlocal t_reservation, t_resline, bresline, buf_rline, rbuff, rline, resline, zinrbuff, mbuff, buffplan, qsy, zbuff

        datum:date = None
        upto_date:date = None
        i:int = 0
        iftask:str = ""
        origcode:str = ""
        do_it:bool = False
        cat_flag:bool = False
        roomnr:int = 0
        Qsy = Queasy
        Zbuff = Zimkateg

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == new_resno) &  (Res_line.reslinnr == reslinno)).first()
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(iftask, 0, 10) == "$origcode$":
                origcode = substring(iftask, 10)
                return

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
            upto_date = res_line.abreise - 1
        for datum in range(res_line.ankunft,upto_date + 1) :

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 171) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (Queasy.char1 == "")).first()

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()

                if qsy:
                    qsy.logi2 = True

                    qsy = db_session.query(Qsy).first()


            if origcode != "":

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 171) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (func.lower(Queasy.char1) == (origcode).lower())).first()

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    qsy = db_session.query(Qsy).filter(
                            (Qsy._recid == queasy._recid)).first()

                    if qsy:
                        qsy.logi2 = True

                        qsy = db_session.query(Qsy).first()


    ci_date = get_output(htpdate(87))

    if deposit_flag:

        for reservation in db_session.query(Reservation).all():
            new_resno = reservation.resnr + 1


            break

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()

        if reservation:
            t_reservation = T_reservation()
            db_session.add(t_reservation)

            buffer_copy(reservation, t_reservation,except_fields=["reservation.resnr"])
            t_reservation.resnr = new_resno
            t_reservation.depositbez = 0
            t_reservation.depositgef = 0

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

        if res_line:
            t_resline = T_resline()
            db_session.add(t_resline)

            buffer_copy(res_line, t_resline,except_fields=["res_line.resnr"])
            t_resline.resnr = new_resno

        bresline = db_session.query(Bresline).filter(
                (Bresline.resnr == new_resno)).first()

        if bresline:

            if priscilla_active:
                get_output(intevent_1(12, bresline.zinr, "Priscilla", bresline.resnr, bresline.reslinnr))
            update_resline_copy()
            update_queasy_copy()

        if not all_flag:

            buf_rline = db_session.query(Buf_rline).filter(
                    (Buf_rline.resnr == resno) &  (Buf_rline.reslinnr == reslinno)).first()

            if buf_rline:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "ResChanges"
                reslin_queasy.resnr = buf_rline.resnr
                reslin_queasy.reslinnr = buf_rline.reslinnr
                reslin_queasy.date2 = get_current_date()
                reslin_queasy.number2 = get_current_time_in_seconds()


                reslin_queasy.char3 = to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(buf_rline.name) + ";" + to_string("RE_ACTIVATE RSV") + ";" + to_string(" ") + ";" + to_string(" ") + ";"

                reslin_queasy = db_session.query(Reslin_queasy).first()

        else:

            for buf_rline in db_session.query(Buf_rline).filter(
                    (Buf_rline.resnr == resno)).all():
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "ResChanges"
                reslin_queasy.resnr = buf_rline.resnr
                reslin_queasy.reslinnr = buf_rline.reslinnr
                reslin_queasy.date2 = get_current_date()
                reslin_queasy.number2 = get_current_time_in_seconds()


                reslin_queasy.char3 = to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(buf_rline.name) + ";" + to_string("RE_ACTIVATE RSV") + ";" + to_string(" ") + ";" + to_string(" ") + ";"

                reslin_queasy = db_session.query(Reslin_queasy).first()

    else:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

        if priscilla_active:
            get_output(intevent_1(12, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()
        update_resline()
        update_queasy()

        if not all_flag:

            buf_rline = db_session.query(Buf_rline).filter(
                    (Buf_rline.resnr == resno) &  (Buf_rline.reslinnr == reslinno)).first()

            if buf_rline:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "ResChanges"
                reslin_queasy.resnr = buf_rline.resnr
                reslin_queasy.reslinnr = buf_rline.reslinnr
                reslin_queasy.date2 = get_current_date()
                reslin_queasy.number2 = get_current_time_in_seconds()


                reslin_queasy.char3 = to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(buf_rline.name) + ";" + to_string("RE_ACTIVATE RSV") + ";" + to_string(" ") + ";" + to_string(" ") + ";"

                reslin_queasy = db_session.query(Reslin_queasy).first()

        else:

            for buf_rline in db_session.query(Buf_rline).filter(
                    (Buf_rline.resnr == resno)).all():
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "ResChanges"
                reslin_queasy.resnr = buf_rline.resnr
                reslin_queasy.reslinnr = buf_rline.reslinnr
                reslin_queasy.date2 = get_current_date()
                reslin_queasy.number2 = get_current_time_in_seconds()


                reslin_queasy.char3 = to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.ankunft) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.abreise) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.zimmeranz) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.erwachs) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.kind1) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.gratis) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zikatnr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.zinr) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.arrangement) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(buf_rline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(buf_rline.name) + ";" + to_string("RE_ACTIVATE RSV") + ";" + to_string(" ") + ";" + to_string(" ") + ";"

                reslin_queasy = db_session.query(Reslin_queasy).first()


    return generate_output()