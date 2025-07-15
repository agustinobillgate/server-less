from functions.additional_functions import *
import decimal
from models import Queasy

t_queasy_list, T_queasy = create_model_like(Queasy)

def delete_queasybl(case_type:int, t_queasy_list:[T_queasy]):
    success_flag = False
    queasy = None

    t_queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy
        nonlocal case_type


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"success_flag": success_flag}

    t_queasy = query(t_queasy_list, first=True)

    if case_type == 1:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_queasy.key) &  (Queasy.char1 == t_queasy.char1)).first()

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True


    elif case_type == 2:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_queasy.key) &  (Queasy.number1 == t_queasy.number1)).first()

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True


    elif case_type == 3:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_queasy.key) &  (Queasy.number1 == t_queasy.number1) &  (Queasy.char1 == t_queasy.char1)).first()

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True


    elif case_type == 11:

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == t_queasy.number3)).first()

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True

    return generate_output()