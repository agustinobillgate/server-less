from functions.additional_functions import *
import decimal
from models import Hoteldpt

def write_hoteldptbl(case_type:int, t_hoteldpt:[T_hoteldpt]):
    success_flag = False
    hoteldpt = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, hoteldpt


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"success_flag": success_flag}

    t_hoteldpt = query(t_hoteldpt_list, first=True)

    if not t_hoteldpt:

        return generate_output()

    if case_type == 1:
        hoteldpt = Hoteldpt()
        db_session.add(hoteldpt)

        buffer_copy(t_hoteldpt, hoteldpt)

        success_flag = True


    elif case_type == 2:

        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.num == t_Hoteldpt.num)).first()

        if hoteldpt:
            buffer_copy(t_hoteldpt, hoteldpt)

            success_flag = True

    return generate_output()