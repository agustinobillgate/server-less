from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Bediener, Res_history, Reslin_queasy

def flag_reportbl(case_type:int, n:int, resnr:int, reslinnr:int, user_init:str, s_list:[S_list]):
    i:int = 0
    k:int = 0
    res_line = bediener = res_history = reslin_queasy = None

    s_list = sbuff = None

    s_list_list, S_list = create_model("S_list", {"newflag":bool, "id":str, "frdate":date, "datum":date, "note":str, "urgent":bool, "done":bool, "dept":str, "ciflag":bool, "coflag":bool}, {"newflag": True})
    sbuff_list, Sbuff = create_model_like(S_list)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, k, res_line, bediener, res_history, reslin_queasy


        nonlocal s_list, sbuff
        nonlocal s_list_list, sbuff_list
        return {}


    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    s_list = query(s_list_list, first=True)

    if case_type == 1:

        if res_line:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Flag Report deleted: " + res_line.name +\
                    " ResNo: " + to_string(res_line.resnr) +\
                    " RmNo: " + res_line.zinr +\
                    " Date: " + to_string(s_list.datum) +\
                    " Note: " + s_list.note
            res_history.action = "Flag Report"

            res_history = db_session.query(Res_history).first()

    elif case_type == 2:

        s_list = query(s_list_list, filters=(lambda s_list :s_list.datum != None), first=True)

        if not s_list:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "flag") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.reslinnr == reslinnr) &  (Reslin_queasy.betriebsnr == n)).first()

            if reslin_queasy:
                db_session.delete(reslin_queasy)
        else:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "flag") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.reslinnr == reslinnr) &  (Reslin_queasy.betriebsnr == n)).first()

            if not reslin_queasy:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "flag"
                reslin_queasy.resnr = resnr
                reslin_queasy.reslinnr = reslinnr
                reslin_queasy.betriebsnr = n


            reslin_queasy.date1 = None
            reslin_queasy.char1 = ""
            reslin_queasy.number1 = 0
            reslin_queasy.deci1 = 0
            reslin_queasy.date2 = None
            reslin_queasy.char2 = ""
            reslin_queasy.number2 = 0
            reslin_queasy.deci2 = 0
            reslin_queasy.date3 = None
            reslin_queasy.char3 = ""
            reslin_queasy.number3 = 0
            reslin_queasy.deci3 = 0


            k = (reslin_queasy.betriebsnr * 3) + 1
            i = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.datum != None and i < (k + 3))):
                i = i + 1

                if i == k:
                    reslin_queasy.date1 = s_list.datum
                    reslin_queasy.char1 = s_list.note +\
                            chr(2) + entry(0, s_list.id, chr(2))

                    if s_list.id == "" and s_list.newflag:
                        reslin_queasy.char1 = reslin_queasy.char1 + bediener.userinit
                    reslin_queasy.char1 = reslin_queasy.char1 +\
                            chr(2) + to_string(get_month(s_list.frdate) , "99") +\
                            to_string(get_day(s_list.frdate) , "99") +\
                            to_string(get_year(s_list.frdate)) +\
                            chr(2) + s_list.dept +\
                            chr(2) + to_string(to_int(s_list.ciflag))
                    reslin_queasy.logi1 = s_list.coflag
                    reslin_queasy.number1 = to_int(s_list.urgent)
                    reslin_queasy.deci1 = to_int(s_list.done)

                    if num_entries(s_list.id, chr(2)) > 1:
                        reslin_queasy.char1 = reslin_queasy.char1 +\
                            chr(2) + entry(1, s_list.id, chr(2))

                if i == (k + 1):
                    reslin_queasy.date2 = s_list.datum
                    reslin_queasy.char2 = s_list.note +\
                            chr(2) + entry(0, s_list.id, chr(2))

                    if s_list.id == "":
                        reslin_queasy.char2 = reslin_queasy.char2 + bediener.userinit
                    reslin_queasy.char2 = reslin_queasy.char2 +\
                            chr(2) + to_string(get_month(s_list.frdate) , "99") +\
                            to_string(get_day(s_list.frdate) , "99") +\
                            to_string(get_year(s_list.frdate)) +\
                            chr(2) + s_list.dept +\
                            chr(2) + to_string(to_int(s_list.ciflag))
                    reslin_queasy.logi2 = s_list.coflag
                    reslin_queasy.number2 = to_int(s_list.urgent)
                    reslin_queasy.deci2 = to_int(s_list.done)

                    if num_entries(s_list.id, chr(2)) > 1:
                        reslin_queasy.char2 = reslin_queasy.char2 +\
                            chr(2) + entry(1, s_list.id, chr(2))

                if i == (k + 2):
                    reslin_queasy.date3 = s_list.datum
                    reslin_queasy.char3 = s_list.note +\
                            chr(2) + entry(0, s_list.id, chr(2))

                    if s_list.id == "":
                        reslin_queasy.char3 = reslin_queasy.char3 + bediener.userinit
                    reslin_queasy.char3 = reslin_queasy.char3 +\
                            chr(2) + to_string(get_month(s_list.frdate) , "99") +\
                            to_string(get_day(s_list.frdate) , "99") +\
                            to_string(get_year(s_list.frdate)) +\
                            chr(2) + s_list.dept +\
                            chr(2) + to_string(to_int(s_list.ciflag))
                    reslin_queasy.logi3 = s_list.coflag
                    reslin_queasy.number3 = to_int(s_list.urgent)
                    reslin_queasy.deci3 = to_int(s_list.done)

                    if num_entries(s_list.id, chr(2)) > 1:
                        reslin_queasy.char3 = reslin_queasy.char3 +\
                            chr(2) + entry(1, s_list.id, chr(2))

    return generate_output()