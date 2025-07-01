#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Fixleist, Reslin_queasy, Res_line

def delete_fixleist_webbl(case_type:int, int1:int, user_init:string):

    prepare_cache ([Reslin_queasy, Res_line])

    succesflag = False
    is_fixrate:string = "False"
    fixleist = reslin_queasy = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal succesflag, is_fixrate, fixleist, reslin_queasy, res_line
        nonlocal case_type, int1, user_init

        return {"succesflag": succesflag}

    def res_changes():

        nonlocal succesflag, is_fixrate, fixleist, reslin_queasy, res_line
        nonlocal case_type, int1, user_init

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


        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("Fixcost DELETED:") + ";" + to_string(fixleist.artnr) + "-" + to_string(fixleist.bezeich) + ";" + to_string(is_fixrate, "x(3)") + ";" + to_string(is_fixrate, "x(3)") + ";"
        pass
        pass

    if case_type == 1:

        fixleist = get_cache (Fixleist, {"_recid": [(eq, int1)]})

        if fixleist:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, fixleist.resnr)],"reslinnr": [(eq, fixleist.reslinnr)]})

            if reslin_queasy:
                is_fixrate = "YES"

            res_line = get_cache (Res_line, {"resnr": [(eq, fixleist.resnr)],"reslinnr": [(eq, fixleist.reslinnr)]})
            res_changes()
            db_session.delete(fixleist)
            pass
            succesflag = True

    return generate_output()