from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Res_line, Zimmer

def ts_tbplan_fl_codebl(case_type:int, int1:int, int2:int, curr_room:str):
    room = ""
    res_line = zimmer = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal room, res_line, zimmer


        return {"room": room}


    if case_type == 1:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == int1) &  (Res_line.reslinnr == int2)).first()

        if res_line:
            room = res_line.zinr

    elif case_type == 2:

        zimmer = db_session.query(Zimmer).filter(
                (func.lower(Zimmer.zinr) == (curr_room).lower())).first()

        if zimmer:
            room = curr_room

    return generate_output()