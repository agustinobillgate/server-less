#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_queasy_data, T_queasy = create_model_like(Queasy)

def delete_queasybl(case_type:int, t_queasy_data:[T_queasy]):
    success_flag = False
    queasy = None

    t_queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy
        nonlocal case_type


        nonlocal t_queasy

        return {"success_flag": success_flag}

    t_queasy = query(t_queasy_data, first=True)

    if case_type == 1:

        queasy = get_cache (Queasy, {"key": [(eq, t_queasy.key)],"char1": [(eq, t_queasy.char1)]})

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True


    elif case_type == 2:

        queasy = get_cache (Queasy, {"key": [(eq, t_queasy.key)],"number1": [(eq, t_queasy.number1)]})

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True


    elif case_type == 3:

        queasy = get_cache (Queasy, {"key": [(eq, t_queasy.key)],"number1": [(eq, t_queasy.number1)],"char1": [(eq, t_queasy.char1)]})

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True


    elif case_type == 11:

        queasy = get_cache (Queasy, {"_recid": [(eq, t_queasy.number3)]})

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True

    return generate_output()