from functions.additional_functions import *
import decimal
from models import Queasy

def delete_queasybl(case_type:int, t_queasy:[T_queasy]):
    success_flag = False
    queasy = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"success_flag": success_flag}

    t_queasy = query(t_queasy_list, first=True)

    if case_type == 1:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_Queasy.key) &  (Queasy.char1 == t_Queasy.char1)).first()

        if queasy:
            db_session.delete(queasy)

            success_flag = True


    elif case_type == 2:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_Queasy.key) &  (Queasy.number1 == t_Queasy.number1)).first()

        if queasy:
            db_session.delete(queasy)

            success_flag = True


    elif case_type == 3:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_Queasy.key) &  (Queasy.number1 == t_Queasy.number1) &  (Queasy.char1 == t_Queasy.char1)).first()

        if queasy:
            db_session.delete(queasy)

            success_flag = True


    elif case_type == 11:

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == t_Queasy.number3)).first()

        if queasy:
            db_session.delete(queasy)

            success_flag = True

    return generate_output()