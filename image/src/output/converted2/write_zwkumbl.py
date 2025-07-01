#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Zwkum

t_zwkum_list, T_zwkum = create_model_like(Zwkum)

def write_zwkumbl(case_type:int, t_zwkum_list:[T_zwkum]):
    success_flag = False
    zwkum = None

    t_zwkum = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, zwkum
        nonlocal case_type


        nonlocal t_zwkum

        return {"success_flag": success_flag}

    t_zwkum = query(t_zwkum_list, first=True)

    if not t_zwkum:

        return generate_output()

    if case_type == 1:
        zwkum = Zwkum()
        db_session.add(zwkum)

        buffer_copy(t_zwkum, zwkum)
        pass
        success_flag = True
    elif case_type == 2:

        zwkum = get_cache (Zwkum, {"zknr": [(eq, t_zwkum.zknr)],"departement": [(eq, t_zwkum.departement)]})

        if zwkum:
            buffer_copy(t_zwkum, zwkum)
            pass
            success_flag = True
    elif case_type == 3:

        zwkum = get_cache (Zwkum, {"zknr": [(eq, t_zwkum.zknr)],"departement": [(eq, t_zwkum.departement)]})

        if zwkum:
            db_session.delete(zwkum)
            pass
            success_flag = True

    return generate_output()