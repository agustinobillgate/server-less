from functions.additional_functions import *
import decimal
from models import Hoteldpt

def read_hoteldptbl(deptno:int):
    t_hoteldpt_list = []
    hoteldpt = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_hoteldpt_list, hoteldpt


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"t-hoteldpt": t_hoteldpt_list}

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == deptno)).first()

    if hoteldpt:
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()