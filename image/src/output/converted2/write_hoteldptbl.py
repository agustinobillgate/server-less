#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt

t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)

def write_hoteldptbl(case_type:int, t_hoteldpt_list:[T_hoteldpt]):
    success_flag = False
    hoteldpt = None

    t_hoteldpt = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, hoteldpt
        nonlocal case_type


        nonlocal t_hoteldpt

        return {"success_flag": success_flag}

    t_hoteldpt = query(t_hoteldpt_list, first=True)

    if not t_hoteldpt:

        return generate_output()

    if case_type == 1:
        hoteldpt = Hoteldpt()
        db_session.add(hoteldpt)

        buffer_copy(t_hoteldpt, hoteldpt)
        pass
        success_flag = True


    elif case_type == 2:

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, t_hoteldpt.num)]})

        if hoteldpt:
            buffer_copy(t_hoteldpt, hoteldpt)
            pass
            success_flag = True

    return generate_output()