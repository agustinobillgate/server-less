#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt

def read_hoteldptbl(deptno:int):
    t_hoteldpt_list = []
    hoteldpt = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_hoteldpt_list, hoteldpt
        nonlocal deptno


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        return {"t-hoteldpt": t_hoteldpt_list}

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, deptno)]})

    if hoteldpt:
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()