#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt

def prepare_h_2ndpricebl():
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

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()