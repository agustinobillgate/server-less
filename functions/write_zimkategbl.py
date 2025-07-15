#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg

t_zimkateg_data, T_zimkateg = create_model_like(Zimkateg)

def write_zimkategbl(case_type:int, t_zimkateg_data:[T_zimkateg]):
    success_flag = False
    zimkateg = None

    t_zimkateg = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, zimkateg
        nonlocal case_type


        nonlocal t_zimkateg

        return {"success_flag": success_flag}

    t_zimkateg = query(t_zimkateg_data, first=True)

    if not t_zimkateg:

        return generate_output()

    if case_type == 1:
        zimkateg = Zimkateg()
        db_session.add(zimkateg)

        buffer_copy(t_zimkateg, zimkateg)
        pass
        success_flag = True


    elif case_type == 2:

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, t_zimkateg.zikatnr)]})

        if zimkateg:
            buffer_copy(t_zimkateg, zimkateg)
            pass
            success_flag = True

    return generate_output()