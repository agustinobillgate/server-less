from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Akt_code

t_akt_code_list, T_akt_code = create_model_like(Akt_code)

def akt_rivaladminbl(pvilanguage:int, case_type:int, t_akt_code_list:[T_akt_code], aktionscode:int, aktiongrup:int, bezeich:str):
    msg_str = ""
    success_flag = False
    lvcarea:str = "akt_rivaladmin"
    akt_code = None

    t_akt_code = akt_code1 = None

    Akt_code1 = Akt_code

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, lvcarea, akt_code
        nonlocal akt_code1


        nonlocal t_akt_code, akt_code1
        nonlocal t_akt_code_list
        return {"msg_str": msg_str, "success_flag": success_flag}

    def fill_akt_code():

        nonlocal msg_str, success_flag, lvcarea, akt_code
        nonlocal akt_code1


        nonlocal t_akt_code, akt_code1
        nonlocal t_akt_code_list


        akt_code.aktiongrup = 4
        akt_code.aktionscode = t_akt_code.aktionscode
        akt_code.bezeich = t_akt_code.bezeich
        akt_code.bemerkung = t_akt_code.bemerkung

    def validate_it():

        nonlocal msg_str, success_flag, lvcarea, akt_code
        nonlocal akt_code1


        nonlocal t_akt_code, akt_code1
        nonlocal t_akt_code_list

        akt_code1 = db_session.query(Akt_code1).filter(
                (Akt_code1.bezeich == t_akt_code.bezeich) &  (Akt_code1.aktionscode != t_akt_code.aktionscode)).first()

        if akt_code1:
            msg_str = msg_str + chr(2) + "&W" + translateExtended ("Other Competitor Name exists with the same description.", lvcarea, "")

        akt_code1 = db_session.query(Akt_code1).filter(
                (Akt_code1.bezeich == t_akt_code.bezeich) &  (Akt_code1.aktionscode != t_akt_code.aktionscode)).first()

        if akt_code1:
            msg_str = msg_str + chr(2) + "&W" + translateExtended ("Other Competitor Name exists with the same description.", lvcarea, "")

    t_akt_code = query(t_akt_code_list, first=True)
    validate_it()

    if case_type == 1:
        akt_code = Akt_code()
        db_session.add(akt_code)

        fill_akt_code()
        success_flag = True

    elif case_type == 2:

        akt_code = db_session.query(Akt_code).filter(
                (Akt_code.aktiongrup == aktiongrup) &  (Akt_code.aktionscode == aktionscode) &  (func.lower(Akt_code.bezeich) == (bezeich).lower())).first()

        if akt_code:
            fill_akt_code()
            success_flag = True

    return generate_output()