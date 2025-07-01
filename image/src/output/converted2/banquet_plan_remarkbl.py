#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.ba_plan_btn_notebl import ba_plan_btn_notebl
from functions.edit_baresnotebl import edit_baresnotebl
from functions.update_baresnotebl import update_baresnotebl

def banquet_plan_remarkbl(rml_raum:string, rml_nr:int, rml_resnr:int, case_type:int, remark:string):
    mess_str = ""
    curr_room:string = ""
    curr_status:int = 0
    t_veran_nr:int = 0
    avail_mainres:bool = False

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str, curr_room, curr_status, t_veran_nr, avail_mainres
        nonlocal rml_raum, rml_nr, rml_resnr, case_type, remark

        return {"mess_str": mess_str, "remark": remark}

    curr_room = rml_raum
    curr_status = rml_nr

    if case_type == 1:
        t_veran_nr, avail_mainres = get_output(ba_plan_btn_notebl(rml_resnr))

        if avail_mainres:
            remark = get_output(edit_baresnotebl(rml_resnr))
        else:
            mess_str = "Main Reservation Unavailable!"

            return generate_output()

    elif case_type == 2:
        get_output(update_baresnotebl(rml_resnr, remark))

    return generate_output()