#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Zimmer

def ts_tbplan_fl_codebl(case_type:int, int1:int, int2:int, curr_room:string):

    prepare_cache ([Res_line])

    room = ""
    res_line = zimmer = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room, res_line, zimmer
        nonlocal case_type, int1, int2, curr_room

        return {"room": room}


    if case_type == 1:

        res_line = get_cache (Res_line, {"resnr": [(eq, int1)],"reslinnr": [(eq, int2)]})

        if res_line:
            room = res_line.zinr

    elif case_type == 2:

        zimmer = get_cache (Zimmer, {"zinr": [(eq, curr_room)]})

        if zimmer:
            room = curr_room

    return generate_output()