#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Zimkateg, Zimmer, Resplan, Zimplan, Guest, Reslin_queasy

def res_assign_zibl(resnr:int, reslinnr:int, rmcat:string, ses_param:string, user_init:string, zinr:string):

    prepare_cache ([Htparam, Res_line, Zimkateg, Zimmer, Resplan, Zimplan, Reslin_queasy])

    msg_str = ""
    ci_date:date = None
    htparam = res_line = zimkateg = zimmer = resplan = zimplan = guest = reslin_queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal resnr, reslinnr, rmcat, ses_param, user_init, zinr

        return {"msg_str": msg_str}

    def enter_room():

        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal resnr, reslinnr, rmcat, ses_param, user_init, zinr

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"zinr": [(eq, "")],"active_flag": [(eq, 0)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg.kurzbez.lower()  != (rmcat).lower() :
            min_resplan()
        update_resline()
        assign_zinr()
        res_changes()

        if zimkateg.kurzbez.lower()  != (rmcat).lower() :
            add_resplan()


    def update_resline():

        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal resnr, reslinnr, rmcat, ses_param, user_init, zinr

        zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})
        res_line.zikatnr = zimmer.zikatnr
        res_line.zinr = zimmer.zinr
        res_line.setup = zimmer.setup
        res_line.reserve_char = to_string(get_current_date()) + to_string(get_current_time_in_seconds(), "HH:MM") + user_init
        res_line.changed = ci_date
        res_line.changed_id = user_init


        pass


    def min_resplan():

        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal resnr, reslinnr, rmcat, ses_param, user_init, zinr

        curr_date:date = None
        curr_date = res_line.ankunft
        while curr_date >= res_line.ankunft and curr_date < res_line.abreise:

            resplan = get_cache (Resplan, {"zikatnr": [(eq, zimkateg.zikatnr)],"datum": [(eq, curr_date)]})

            if resplan:
                pass
                resplan.anzzim[res_line.resstatus - 1] = resplan.anzzim[res_line.resstatus - 1] - res_line.zimmeranz
                pass
                pass
            curr_date = curr_date + timedelta(days=1)


    def add_resplan():

        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal resnr, reslinnr, rmcat, ses_param, user_init, zinr

        curr_date:date = None
        zbuff = None
        Zbuff =  create_buffer("Zbuff",Zimkateg)

        zbuff = get_cache (Zimkateg, {"kurzbez": [(eq, rmcat)]})
        curr_date = res_line.ankunft
        while curr_date >= res_line.ankunft and curr_date < res_line.abreise:

            resplan = get_cache (Resplan, {"zikatnr": [(eq, zbuff.zikatnr)],"datum": [(eq, curr_date)]})

            if resplan:
                pass
                resplan.anzzim[res_line.resstatus - 1] = resplan.anzzim[res_line.resstatus - 1] + res_line.zimmeranz
                pass
                pass
            curr_date = curr_date + timedelta(days=1)


    def assign_zinr():

        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal resnr, reslinnr, rmcat, ses_param, user_init, zinr

        curr_datum:date = None

        if zinr != "" and not (res_line.resstatus == 11):
            for curr_datum in date_range(res_line.ankunft,(res_line.abreise - 1)) :

                zimplan = get_cache (Zimplan, {"datum": [(eq, curr_datum)],"zinr": [(eq, zinr)]})

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


                    pass
                    pass


    def res_changes():

        nonlocal msg_str, ci_date, htparam, res_line, zimkateg, zimmer, resplan, zimplan, guest, reslin_queasy
        nonlocal resnr, reslinnr, rmcat, ses_param, user_init, zinr

        do_it:bool = False
        cid:string = " "
        cdate:string = " "
        guest1 = None
        Guest1 =  create_buffer("Guest1",Guest)

        if trim(res_line.changed_id) != "":
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)

        elif length(res_line.reserve_char) >= 14:
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
        pass
        pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    enter_room()

    return generate_output()