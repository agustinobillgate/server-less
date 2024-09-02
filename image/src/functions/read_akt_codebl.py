from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Akt_code

def read_akt_codebl(case_type:int, bezeich:str, aktionscode:int):
    t_akt_code_list = []
    akt_code = None

    t_akt_code = None

    t_akt_code_list, T_akt_code = create_model_like(Akt_code)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_akt_code_list, akt_code


        nonlocal t_akt_code
        nonlocal t_akt_code_list
        return {"t-akt-code": t_akt_code_list}

    if case_type == 1:

        for akt_code in db_session.query(Akt_code).filter(
                (Akt_code.aktiongrup == 1)).all():
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 2:

        # akt_code = db_session.query(Akt_code).filter(
        #         (Akt_code.aktiongrup == 1) &  (func.lower(Akt_code.(bezeich).lower()) == (bezeich).lower())).first()

        akt_code = db_session.query(Akt_code).filter(
                (Akt_code.aktiongrup == 1) &  (func.lower(Akt_code.bezeich) == bezeich.lower())).first()
        
        if akt_code:
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 3:

        akt_code = db_session.query(Akt_code).filter(
                (Akt_code.aktionscode == aktionscode)).first()

        if akt_code:
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 4:

        akt_code = db_session.query(Akt_code).filter(
                (Akt_code.aktiongrup == 1) &  (Akt_code.aktionscode == aktionscode)).first()

        if akt_code:
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 5:

        for akt_code in db_session.query(Akt_code).all():
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 6:

        akt_code = db_session.query(Akt_code).filter(
                (Akt_code.aktiongrup == 2) &  (Akt_code.aktionscode == 1)).first()

        if akt_code:
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 7:

        # akt_code = db_session.query(Akt_code).filter(
        #         (Akt_code.aktiongrup == aktionscode) &  (func.lower(Akt_code.(bezeich).lower()) == (bezeich).lower())).first()
        akt_code = db_session.query(Akt_code).filter(
                (Akt_code.aktiongrup == aktionscode) &  (func.lower(Akt_code.bezeich) == bezeich.lower())).first()
        if akt_code:
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 8:

        akt_code = db_session.query(Akt_code).filter(
                (Akt_code.aktiongrup == 4) &  (Akt_code.aktionscode == aktionscode)).first()

        if akt_code:
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 9:

        for akt_code in db_session.query(Akt_code).filter(
                (Akt_code.aktiongrup == aktionscode)).all():
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)

    return generate_output()