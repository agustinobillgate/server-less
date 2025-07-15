#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Bediener, Res_history, Reslin_queasy

s_list_data, S_list = create_model("S_list", {"newflag":bool, "id":string, "frdate":date, "datum":date, "note":string, "urgent":bool, "done":bool, "dept":string, "ciflag":bool, "coflag":bool, "rsv_detail":bool, "bill_flag":bool}, {"newflag": True})

def flag_report_1bl(case_type:int, n:int, resnr:int, reslinnr:int, user_init:string, s_list_data:[S_list]):

    prepare_cache ([Res_line, Bediener, Res_history])

    i:int = 0
    k:int = 0
    res_line = bediener = res_history = reslin_queasy = None

    s_list = sbuff = None

    sbuff_data, Sbuff = create_model_like(S_list)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, k, res_line, bediener, res_history, reslin_queasy
        nonlocal case_type, n, resnr, reslinnr, user_init


        nonlocal s_list, sbuff
        nonlocal sbuff_data

        return {}


    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    s_list = query(s_list_data, first=True)

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


            pass
            pass
    elif case_type == 2:

        s_list = query(s_list_data, filters=(lambda s_list: s_list.datum != None), first=True)

        if not s_list:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "flag")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"betriebsnr": [(eq, n)]})

            if reslin_queasy:
                db_session.delete(reslin_queasy)
        else:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "flag")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"betriebsnr": [(eq, n)]})

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
            reslin_queasy.deci1 =  to_decimal("0")
            reslin_queasy.date2 = None
            reslin_queasy.char2 = ""
            reslin_queasy.number2 = 0
            reslin_queasy.deci2 =  to_decimal("0")
            reslin_queasy.date3 = None
            reslin_queasy.char3 = ""
            reslin_queasy.number3 = 0
            reslin_queasy.deci3 =  to_decimal("0")


            k = (reslin_queasy.betriebsnr * 3) + 1
            i = 0

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.datum != None and i < (k + 3)), sort_by=[("datum",False)]):
                i = i + 1

                if i == k:
                    reslin_queasy.date1 = s_list.datum
                    reslin_queasy.char1 = s_list.note +\
                            chr_unicode(2) + s_list.id

                    if s_list.id == "" and s_list.newflag:
                        reslin_queasy.char1 = reslin_queasy.char1 + bediener.userinit
                    reslin_queasy.char1 = reslin_queasy.char1 +\
                            chr_unicode(2) + to_string(get_month(s_list.frdate) , "99") +\
                            to_string(get_day(s_list.frdate) , "99") +\
                            to_string(get_year(s_list.frdate)) +\
                            chr_unicode(2) + s_list.dept +\
                            chr_unicode(2) + to_string(to_int(s_list.ciflag)) +\
                            chr_unicode(2) + to_string(to_int(s_list.rsv_detail)) +\
                            chr_unicode(2) + to_string(to_int(s_list.bill_flag))
                    reslin_queasy.logi1 = s_list.coflag
                    reslin_queasy.number1 = to_int(s_list.urgent)
                    reslin_queasy.deci1 =  to_decimal(to_int(s_list.done) )

                if i == (k + 1):
                    reslin_queasy.date2 = s_list.datum
                    reslin_queasy.char2 = s_list.note +\
                            chr_unicode(2) + s_list.id

                    if s_list.id == "":
                        reslin_queasy.char2 = reslin_queasy.char2 + bediener.userinit
                    reslin_queasy.char2 = reslin_queasy.char2 +\
                            chr_unicode(2) + to_string(get_month(s_list.frdate) , "99") +\
                            to_string(get_day(s_list.frdate) , "99") +\
                            to_string(get_year(s_list.frdate)) +\
                            chr_unicode(2) + s_list.dept +\
                            chr_unicode(2) + to_string(to_int(s_list.ciflag)) +\
                            chr_unicode(2) + to_string(to_int(s_list.rsv_detail)) +\
                            chr_unicode(2) + to_string(to_int(s_list.bill_flag))
                    reslin_queasy.logi2 = s_list.coflag
                    reslin_queasy.number2 = to_int(s_list.urgent)
                    reslin_queasy.deci2 =  to_decimal(to_int(s_list.done) )

                if i == (k + 2):
                    reslin_queasy.date3 = s_list.datum
                    reslin_queasy.char3 = s_list.note +\
                            chr_unicode(2) + s_list.id

                    if s_list.id == "":
                        reslin_queasy.char3 = reslin_queasy.char3 + bediener.userinit
                    reslin_queasy.char3 = reslin_queasy.char3 +\
                            chr_unicode(2) + to_string(get_month(s_list.frdate) , "99") +\
                            to_string(get_day(s_list.frdate) , "99") +\
                            to_string(get_year(s_list.frdate)) +\
                            chr_unicode(2) + s_list.dept +\
                            chr_unicode(2) + to_string(to_int(s_list.ciflag)) +\
                            chr_unicode(2) + to_string(to_int(s_list.rsv_detail)) +\
                            chr_unicode(2) + to_string(to_int(s_list.bill_flag))
                    reslin_queasy.logi3 = s_list.coflag
                    reslin_queasy.number3 = to_int(s_list.urgent)
                    reslin_queasy.deci3 =  to_decimal(to_int(s_list.done) )

    return generate_output()