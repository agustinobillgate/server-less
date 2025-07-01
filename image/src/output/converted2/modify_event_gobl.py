#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ba_plan_btn_timebl import ba_plan_btn_timebl
from functions.ba_plan_btn_roombl import ba_plan_btn_roombl
from functions.ba_plan_btn_stat2_1bl import ba_plan_btn_stat2_1bl

def modify_event_gobl(rml_resnr:int, rml_reslinnr:int, user_init:string, chg_date:date, begin_time:string, ending_time:string, begin_i:int, ending_i:int, chg_room:string, chg_table:string, c_status:string, r_status:int, recid_rl:int, bk_reser_resstatus:int):
    mess_str = ""

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str
        nonlocal rml_resnr, rml_reslinnr, user_init, chg_date, begin_time, ending_time, begin_i, ending_i, chg_room, chg_table, c_status, r_status, recid_rl, bk_reser_resstatus

        return {"mess_str": mess_str}

    get_output(ba_plan_btn_timebl(rml_resnr, rml_reslinnr, user_init, chg_date, begin_time, ending_time, begin_i, ending_i))
    get_output(ba_plan_btn_roombl(rml_resnr, rml_reslinnr, chg_room, user_init, chg_table))
    get_output(ba_plan_btn_stat2_1bl(False, rml_resnr, rml_reslinnr, c_status, r_status, recid_rl, bk_reser_resstatus, user_init))
    mess_str = "Modify Event Done"

    return generate_output()