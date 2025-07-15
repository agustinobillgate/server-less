#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Hoteldpt

def pos_dashboard_prepare_odcancelbl():
    bill_date = None
    t_hoteldpt_data = []
    hoteldpt = None

    t_hoteldpt = None

    t_hoteldpt_data, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, t_hoteldpt_data, hoteldpt


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_data

        return {"bill_date": bill_date, "t-hoteldpt": t_hoteldpt_data}


    bill_date = get_output(htpdate(110))

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num >= 1)).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_data.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()