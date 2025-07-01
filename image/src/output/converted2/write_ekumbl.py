#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Ekum

t_ekum_list, T_ekum = create_model_like(Ekum)

def write_ekumbl(case_type:int, t_ekum_list:[T_ekum]):
    success_flag = False
    ekum = None

    t_ekum = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, ekum
        nonlocal case_type


        nonlocal t_ekum

        return {"success_flag": success_flag}

    t_ekum = query(t_ekum_list, first=True)

    if not t_ekum:

        return generate_output()

    if case_type == 1:
        ekum = Ekum()
        db_session.add(ekum)

        buffer_copy(t_ekum, ekum)
        pass
        success_flag = True
    elif case_type == 2:

        ekum = get_cache (Ekum, {"eknr": [(eq, t_ekum.eknr)]})

        if ekum:
            buffer_copy(t_ekum, ekum)
            pass
            success_flag = True

    return generate_output()