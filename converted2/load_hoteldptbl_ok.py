from functions.additional_functions import *
import decimal
from models import Hoteldpt

def load_hoteldptbl():
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

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()