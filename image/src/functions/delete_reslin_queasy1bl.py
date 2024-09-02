from functions.additional_functions import *
import decimal
from datetime import date
from models import Reslin_queasy, Res_line

def delete_reslin_queasy1bl(case_type:int, int1:int, char1:str, date1:date):
    success_flag = False
    user_init:str = ""
    reslin_queasy = res_line = None

    rqy = None

    Rqy = Reslin_queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, user_init, reslin_queasy, res_line
        nonlocal rqy


        nonlocal rqy
        return {"success_flag": success_flag}

    def res_changes():

        nonlocal success_flag, user_init, reslin_queasy, res_line
        nonlocal rqy


        nonlocal rqy

        cid:str = ""
        cdate:str = ""
        Rqy = Reslin_queasy

        if not res_line:

            return

        if res_line.active_flag == 2:

            return

        if res_line.changed != None:
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)


        rqy = Rqy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()


        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("Fixrate DELETED:") + ";" + to_string(reslin_queasy.date1) + "-" + to_string(reslin_queasy.deci1) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"

        rqy = db_session.query(Rqy).first()

    if case_type == 1:
        user_init = char1

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (Reslin_queasy._recid == int1)).first()

        if reslin_queasy:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == reslin_queasy.resnr) &  (Res_line.reslinnr == reslin_queasy.reslinnr)).first()
            res_changes()
            db_session.delete(reslin_queasy)

            success_flag = True

    return generate_output()