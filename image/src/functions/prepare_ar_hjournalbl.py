from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Hoteldpt

def prepare_ar_hjournalbl():
    from_date = None
    t_hoteldpt_list = []
    hoteldpt = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, t_hoteldpt_list, hoteldpt


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"from_date": from_date, "t-hoteldpt": t_hoteldpt_list}


    from_date = get_output(htpdate(110))

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()