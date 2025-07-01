#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy, Res_line

def delete_reslin_queasy1bl(case_type:int, int1:int, char1:string, date1:date):

    prepare_cache ([Reslin_queasy, Res_line])

    success_flag = False
    user_init:string = ""
    reslin_queasy = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, user_init, reslin_queasy, res_line
        nonlocal case_type, int1, char1, date1

        return {"success_flag": success_flag}

    def res_changes():

        nonlocal success_flag, user_init, reslin_queasy, res_line
        nonlocal case_type, int1, char1, date1

        cid:string = ""
        cdate:string = " "
        rqy = None
        Rqy =  create_buffer("Rqy",Reslin_queasy)

        if not res_line:

            return

        if res_line.active_flag == 2:

            return

        if res_line.changed != None:
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)


        rqy = Reslin_queasy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()


        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("Fixrate DELETED:") + ";" + to_string(reslin_queasy.date1) + "-" + to_string(reslin_queasy.deci1) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"
        pass
        pass

    if case_type == 1:
        user_init = char1

        reslin_queasy = get_cache (Reslin_queasy, {"_recid": [(eq, int1)]})

        if reslin_queasy:

            res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)]})
            res_changes()
            db_session.delete(reslin_queasy)
            pass
            success_flag = True

    return generate_output()