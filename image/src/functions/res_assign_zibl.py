from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Res_line, Zimkateg, Zimmer, Resplan, Zimplan, Guest, Reslin_queasy

def res_assign_zibl(resnr:int, reslinnr:int, rmcat:str, ses_param:str, user_init:str, zinr:str):
    msg_str = ""
    ci_date:date = None
    htparam = res_line = zimkateg = zimmer = resplan = zimplan = guest = reslin_queasy = None

    zbuff = guest1 = None

    Zbuff = Zimkateg
    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal zbuff, guest1


        nonlocal zbuff, guest1
        return {"msg_str": msg_str}

    def enter_room():

        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal zbuff, guest1


        nonlocal zbuff, guest1

        res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr) &  (Res_line.zinr == "") &  (Res_line.active_flag == 0)).first()

        zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

        if zimkateg.kurzbez.lower()  != (rmcat).lower() :
            min_resplan()
        update_resline()
        assign_zinr()
        res_changes()

        if zimkateg.kurzbez.lower()  != (rmcat).lower() :
            add_resplan()


    def update_resline():

        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal zbuff, guest1


        nonlocal zbuff, guest1

        zimmer = db_session.query(Zimmer).filter(
                (func.lower(Zimmer.(zinr).lower()) == (zinr).lower())).first()
        res_line.zikatnr = zimmer.zikatnr
        res_line.zinr = zimmer.zinr
        res_line.setup = zimmer.setup
        res_line.reserve_char = to_string(get_current_date()) + to_string(get_current_time_in_seconds(), "HH:MM") + user_init
        res_line.changed = ci_date
        res_line.changed_id = user_init

        res_line = db_session.query(Res_line).first()

    def min_resplan():

        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal zbuff, guest1


        nonlocal zbuff, guest1

        curr_date:date = None
        curr_date = res_line.ankunft
        while curr_date >= res_line.ankunft and curr_date < res_line.abreise:

            resplan = db_session.query(Resplan).filter(
                    (Resplan.zikatnr == zimkateg.zikatnr) &  (Resplan.datum == curr_date)).first()

            if resplan:

                resplan = db_session.query(Resplan).first()
                resplan.anzzim[res_line.resstatus - 1] = resplan.anzzim[res_line.resstatus - 1] - res_line.zimmeranz

                resplan = db_session.query(Resplan).first()

            curr_date = curr_date + 1

    def add_resplan():

        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal zbuff, guest1


        nonlocal zbuff, guest1

        curr_date:date = None
        Zbuff = Zimkateg

        zbuff = db_session.query(Zbuff).filter(
                (func.lower(Zbuff.kurzbez) == (rmcat).lower())).first()
        curr_date = res_line.ankunft
        while curr_date >= res_line.ankunft and curr_date < res_line.abreise:

            resplan = db_session.query(Resplan).filter(
                    (Resplan.zikatnr == zbuff.zikatnr) &  (Resplan.datum == curr_date)).first()

            if resplan:

                resplan = db_session.query(Resplan).first()
                resplan.anzzim[res_line.resstatus - 1] = resplan.anzzim[res_line.resstatus - 1] + res_line.zimmeranz

                resplan = db_session.query(Resplan).first()

            curr_date = curr_date + 1

    def assign_zinr():

        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal zbuff, guest1


        nonlocal zbuff, guest1

        curr_datum:date = None

        if zinr != "" and not (res_line.resstatus == 11):
            for curr_datum in range(res_line.ankunft,(res_line.abreise - 1)  + 1) :

                zimplan = db_session.query(Zimplan).filter(
                        (Zimplan.datum == curr_datum) &  (func.lower(Zimplan.(zinr).lower()) == (zinr).lower())).first()

                if (not zimplan):
                    zimplan = Zimplan()
                    db_session.add(zimplan)

                    zimplan.datum = curr_datum
                    zimplan.zinr = zinr
                    zimplan.res_recid = res_line._recid
                    zimplan.gastnrmember = res_line.gastnrmember
                    zimplan.bemerk = res_line.bemerk
                    zimplan.resstatus = res_line.resstatus
                    zimplan.name = res_line.name

                    zimplan = db_session.query(Zimplan).first()


    def res_changes():

        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal zbuff, guest1


        nonlocal zbuff, guest1

        do_it:bool = False
        cid:str = ""
        cdate:str = ""
        Guest1 = Guest

        if trim(res_line.changed_id) != "":
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)

        elif len(res_line.reserve_char) >= 14:
            cid = substring(res_line.reserve_char, 13)
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = resnr
        reslin_queasy.reslinnr = reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(zimkateg.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + " " + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string(res_line.name) + ";" + to_string(res_line.name) + ";"

        if res_line.was_status == 0:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string(" NO") + ";" + to_string(" NO") + ";"
        else:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES") + ";" + to_string("YES") + ";"

        reslin_queasy = db_session.query(Reslin_queasy).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    enter_room()

    return generate_output()